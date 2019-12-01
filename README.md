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

| Sources of Variance   |   Degrees of Freedom |   Sum of Squares |   Mean Square |   Variance |   Standard deviation | F-value             | P-value                |
|-----------------------|----------------------|------------------|---------------|------------|----------------------|---------------------|------------------------|
| Operator              |                    2 |        1.63035   |    0.815176   |  0.0538033 |             0.231955 | 100.32243949133408  | 2.1613695507793906e-06 |
| Part                  |                    4 |       28.9094    |    7.22734    |  0.802135  |             0.89562  | 889.4582250787796   | 1.264461868544231e-10  |
| Operator by Part      |                    8 |        0.0650044 |    0.00812556 |  0         |             0        | 0.14237598317885578 | 0.9963728209675697     |
| Measurment            |                   30 |        1.71213   |    0.0570711  |  0.0570711 |             0.238896 |                     |                        |
| Total                 |                   44 |       32.3169    |    0.734474   |  0.91301   |             0.955515 |                     |                        |

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
