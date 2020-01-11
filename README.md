# Gauge R&R

[![GitHub](https://github.com/owodunni/gaugernr/workflows/Python%20package/badge.svg)](https://github.com/owodunni/GaugeRnR)
[![PyPi](https://img.shields.io/pypi/v/GaugeRnR)](https://pypi.org/project/GaugeRnR/)
[![License](https://img.shields.io/github/license/owodunni/GaugeRnR)](https://github.com/owodunni/GaugeRnR/blob/master/LICENSE)

## Install

``` console
pip install GaugeRnR
```
## CLI
The package can be used to generate reports from CLI:

```
GaugeRnR -f data/data_mXop.csv -s 3,5,11 -o outDir
```
This generates a html report that is stored in the outDir folder.

Setting the axes parameter is usefull if the data is not structured correct:
```
GaugeRnR -f data/data_opXm.csv -s 5,7,11 -a 2,1,0 -o outDir
```

```
GaugeRnR -h

GaugeRnR.

The input data should be structeted
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

More info: https://pypi.org/project/GaugeRnR/

Usage:
    GaugeRnR -f FILE -s STRUCTURE [-a <AXES>] [-d <DELIMITER>] [-o <FOLDER>] [-g <PARTS>]
    GaugeRnR -h | --help
    GaugeRnR -v | --version

Examples:
    GaugeRnR -f data.csv -s5,7,11 -o report
    GaugeRnR -f data.csv -s5,7,11 -a 1,0,2 -d ,
    GaugeRnR -f data/data_opXm.csv -s 5,7,11 -a 2,1,0 -o outDir

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
from gaugeRnR import GaugeRnR
import numpy as np

# The input should be structeted in a 3d
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

g = GaugeRnR(data)
g.calculate()
print(g.summary())
```

This will result in the following table:

| Sources of Variance   |   DF |     SS |    MS |   Var (σ²) |   Std (σ) | F-value   | P-value   |
|-----------------------|------|--------|-------|------------|-----------|-----------|-----------|
| Operator              |    2 |  1.63  | 0.815 |      0.054 |     0.232 | 100.322   | 0.000     |
| Part                  |    4 | 28.909 | 7.227 |      0.802 |     0.896 | 889.458   | 0.000     |
| Operator by Part      |    8 |  0.065 | 0.008 |      0     |     0     | 0.142     | 0.996     |
| Measurment            |   30 |  1.712 | 0.057 |      0.057 |     0.239 |           |           |
| Total                 |   44 | 32.317 | 0.734 |      0.913 |     0.956 |           |           |

To access the result from the Gauge RnR data directly:

``` python
from gaugeRnR import GaugeRnR, Component, Result

.
.
.

g = GaugeRnR(data)
result = g.calculate()
F = result[Result.F]
>>> print(F[Component.OPERATOR])
100.322
```

For more examples of how to use this library take a look at the [unit tests](https://github.com/owodunni/GaugeRnR/tree/master/tests)!

## Documentations

This GaugeRnR package was built and tested using the resources bellow. If you want to learn more about Gauge RnR and ANOVA they are a great place to start!

* [anova-gage-rr-part-1](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-1)
* [anova-gage-rr-part-2](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-2)
* [Introduction to Statistical Quality Control 6th Edition](https://www.amazon.com/Introduction-Statistical-Quality-Control-Montgomery/dp/0470169923)
