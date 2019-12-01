# GaugeRnR

This GaugeRnR package was built and tested using the following resources:

* [anova-gage-rr-part-1](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-1)
* [anova-gage-rr-part-2](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-2)
* [Introduction to Statistical Quality Control 6th Edition](https://www.amazon.com/Introduction-Statistical-Quality-Control-Montgomery/dp/0470169923)

## Example

The package can be used in the following way:
``` python
from gaugeRnR import GaugeRnR
from data import data

g = GaugeRnR(data)
g.calculate()
print(g)
```

This will result in the following table:

| Sources of Variance   |   DF |     SS |    MS |   Var (σ²) |   Std (σ) | F-value   | P-value   |
|-----------------------|------|--------|-------|------------|-----------|-----------|-----------|
| Operator              |    2 |  1.63  | 0.815 |      0.054 |     0.232 | 100.322   | 0.000     |
| Part                  |    4 | 28.909 | 7.227 |      0.802 |     0.896 | 889.458   | 0.000     |
| Operator by Part      |    8 |  0.065 | 0.008 |      0     |     0     | 0.142     | 0.996     |
| Measurment            |   30 |  1.712 | 0.057 |      0.057 |     0.239 |           |           |
| Total                 |   44 | 32.317 | 0.734 |      0.913 |     0.956 |           |           |

## Install

To install the requirements needed for this package run:

``` console
pip install -r requirements.txt
```

## Build

To test the package run:

``` console
./main.py
```

## Test

``` console
./test.py
```

## Linter

On each commit the CI pipelin runs the flake8 linter.

This can be run locally:

``` console
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

To lint the code we can use autopep8:

``` console
 autopep8 --aggressive --in-place <filename>
```
