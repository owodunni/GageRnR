# Gauge RnR

[![License](https://img.shields.io/github/license/owodunni/GaugeRnR)](https://github.com/simonw/datasette/blob/master/LICENSE)

## Documentations

This GaugeRnR package was built and tested using the resources bellow. If you want to learn more about Gauge RnR and ANOVA they are a great place to start!

* [anova-gage-rr-part-1](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-1)
* [anova-gage-rr-part-2](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-2)
* [Introduction to Statistical Quality Control 6th Edition](https://www.amazon.com/Introduction-Statistical-Quality-Control-Montgomery/dp/0470169923)

## Example

The package can be used in the following way:

``` python
from gaugeRnR import GaugeRnR
import numpy as np

# The input should be structeted in a 3d
# numpy array with shape [operators parts measurements]
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
print(g.toTabulare())
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

For more examples of how to use this library take a look at the [unit tests](https://github.com/owodunni/GaugeRnR/blob/master/tests/test.py)!
