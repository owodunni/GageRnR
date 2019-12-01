#!/usr/bin/env python3
from gaugeRnR import GaugeRnR
from data import data

g = GaugeRnR(data)
g.calculate()
print(g)
