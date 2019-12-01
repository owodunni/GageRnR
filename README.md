# GaugeRnR

This GaugeRnR package was built and tested using the following resources:

* [anova-gage-rr-part-1](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-1)
* [anova-gage-rr-part-2](https://www.spcforexcel.com/knowledge/measurement-systems-analysis/anova-gage-rr-part-2)
* [Introduction to Statistical Quality Control 6th Edition](https://www.amazon.com/Introduction-Statistical-Quality-Control-Montgomery/dp/0470169923)

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
