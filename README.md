# Gage R&R

[![GitHub](https://github.com/owodunni/gageRnR/workflows/Python%20package/badge.svg)](https://github.com/owodunni/GageRnR)
[![PyPi](https://img.shields.io/pypi/v/GageRnR)](https://pypi.org/project/GageRnR/)
[![License](https://img.shields.io/github/license/owodunni/GaugeRnR)](https://github.com/owodunni/GageRnR/blob/master/LICENSE)

## Table of Contents
1. [Install](#Install)
2. [CLI](#CLI)
3. [Example](#Example)
4. [Statistics](#Statistics)

## Install

From PyPi:
``` vim
pip install GageRnR
```

From source:

``` console
pip install -e .
```

Development dependencies:

``` vim
pip install -r pip/requirements-dev.txt
```

## CLI
The package can be used to generate reports from CLI:

```vim
GageRnR -f data/data_mXop.csv -s 3,5,11 -o outDir
```
This generates a html report that is stored in the outDir folder.

Setting the axes parameter is useful if the data is not structured correct:
```vim
GageRnR -f data/data_opXm.csv -s 5,7,11 -a 2,1,0 -o outDir
```
To calculate linearity and bias ground truth is required:
```vim
GageRnR -f data/data_demoGRnR.csv -s 3,10,3 -a 0,2,1 -g 40,42,30,43,29,45,27.5,42,26,35 -o outDir
```

For more help run:

```vim
GageRnR -h
```

```
GageRnR.

The input data should be structured
in a 3d array n[i,j,k] where
i = operator, j = part, k = measurement
Stored to file this data would look:
m1    m2    m3
3.29; 3.41; 3.64  # p1 | o1
2.44; 2.32; 2.42  # p2
3.08; 3.25; 3.07  # p1 | o2
2.53; 1.78; 2.32  # p2
3.04; 2.89; 2.85  # p1 | o3
1.62; 1.87; 2.04  # p2

More info: https://github.com/owodunni/GageRnR

Usage:
    GageRnR -f FILE -s STRUCTURE [-a <AXES>] [-d <DELIMITER>] [-o <FOLDER>] [-g <PARTS>]
    GageRnR -h | --help
    GageRnR -v | --version

Examples:
    GageRnR -f data.csv -s5,7,11 -o report
    GageRnR -f data/data_mXop.csv -s 3,5,11 -o outDir
    GageRnR -f data/data_opXm.csv -s 5,7,11 -a 2,1,0 -o outDir
    GageRnR -f data/data_demoGRnR.csv -s 3,10,3 -a 0,2,1 -g 40,42,30,43,29,45,27.5,42,26,35 -o outDir

Options:
    -f --file=FILE Load input data.
    -s --structure=STRUCTURE Data structure.
        Order should be operators, parts, measurements.
    -a --axes=<AXES>  Order of data axes [default: 0,1,2].
    -d --delimiter=<DELIMITER>  Order of data axes [default: ;].
    -o --output=<FOLDER> Report output directory
    -g --groundTruth=<PARTS> Ground Truth data for parts
    -h --help     Show this screen.
    -v --version  Show version.
```
## Example

The package can be used in the following way:

``` python
from GageRnR import GageRnR
import numpy as np

# The input should be structured in a 3d
# numpy array n[i,j,k] where
# i = operator, j = part, k = measurement
# Example:
#       m1    m2    m3
data = np.array(            #
    [[[3.29, 3.41, 3.64],   # p1 | o1
      [2.44, 2.32, 2.42],   # p2
      [4.34, 4.17, 4.27],   # p3
      [3.47, 3.5, 3.64],    # p4
      [2.2, 2.08, 2.16]],   # p5
     [[3.08, 3.25, 3.07],   # p1 | o2
      [2.53, 1.78, 2.32],   # p2
      [4.19, 3.94, 4.34],   # p3
      [3.01, 4.03, 3.2],    # p4
      [2.44, 1.8, 1.72]],   # p5
     [[3.04, 2.89, 2.85],   # p1 | o3
      [1.62, 1.87, 2.04],   # p2
      [3.88, 4.09, 3.67],   # p3
      [3.14, 3.2, 3.11],    # p4
      [1.54, 1.93, 1.55]]]) # p5

g = GageRnR(data)
g.calculate()
print(g.summary())
```

This will result in the following table:

| Sources of Variance   |   DF |     SS |    MS |   Var (σ²) |   Std (σ) | F-value   | P-value   |
|-----------------------|------|--------|-------|------------|-----------|-----------|-----------|
| Operator              |    2 |  1.63  | 0.815 |      0.054 |     0.232 | 100.322   | 0.000     |
| Part                  |    4 | 28.909 | 7.227 |      0.802 |     0.896 | 889.458   | 0.000     |
| Operator by Part      |    8 |  0.065 | 0.008 |      0     |     0     | 0.142     | 0.996     |
| Measurement            |   30 |  1.712 | 0.057 |      0.057 |     0.239 |           |           |
| Total                 |   44 | 32.317 | 0.734 |      0.913 |     0.956 |           |           |

To access the result from the Gauge RnR data directly:

``` python
from GageRnR import GageRnR, Component, Result

.
.
.

g = GageRnR(data)
result = g.calculate()
F = result[Result.F]
>>> print(F[Component.OPERATOR])
100.322
```

For more examples of how to use this library take a look at the [unit tests](https://github.com/owodunni/GageRnR/tree/master/tests)!

## Statistics

The package can generate the following statistics:

* GageRnR

    Gauge R&R, which stands for gage repeatability and reproducibility, is a statistical tool that measures the amount of variation in the measurement system arising from the measurement device and the people taking the measurement.

    Unfortunately, all measurement data contains a certain percentage of variation. The variation is the difference between the true values and the observed values. The variation represents the amount of measurement error. In addition to measurement error, is the actual product or process variation. When we combine measurement error with product or process variation the resulting value represents the total variation. To assure that our measurement data is accurate we must determine if the amount of variation is acceptable

    If the p value is less than 0.05, it means that the source of variation has a significant impact on the results.

    For more information take a look at:
    * [anova-gage-rr-part-1](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-1)
    * [anova-gage-rr-part-2](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-2)
    * [Introduction to Statistical Quality Control 6th Edition](https://www.amazon.com/Introduction-Statistical-Quality-Control-Montgomery/dp/0470169923)

* Mean, Standard Deviation and bar chart plots.

    To get a better feel for our measurement data we can plot it together with a bar chart and show some characteristic statistics of the data.
* Normality test

    For Gauge R&R to work it is important that our data is normal distributed. If we don't have enough data the it might not be normal distributed. We can test if the data is normal distributed using a Shapiro-Wilk Test. Small values of W are evidence of departure from normality. It is important that our parts are normally distributed. A P-value smaller then 0.05 indicates that the data is not Gaussian.

    For more information take a look at:

    * [Engineering statistics handbook](https://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm)
    * [Normality tests in python](https://machinelearningmastery.com/a-gentle-introduction-to-normality-tests-in-python/)
* Linearity and Bias - requires ground truth data

    Bias and linearity assess the accuracy of a gage.

    * Bias examines the difference between the observed average measurement and a reference value.
    Bias indicates how accurate the gage is when compared to a reference value.
    * Linearity examines how accurate your measurements are through the expected range of the
    measurements. Linearity indicates whether the gage has the same accuracy across all reference values.

    A P-value smaller then 0.05 indicates that a linear equation fits well to the data.

    For more information take a look at:

    * [Measurement System Analysis](http://reliawiki.org/index.php/Measurement_System_Analysis?fbclid=IwAR2uptrlw9MyMaOVLXCOE89GDvN8hNb0qfxgxfxZs7msewQ7ijzqfnGp8oc)
