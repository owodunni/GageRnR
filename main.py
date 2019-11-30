#!/usr/bin/env python3
from generator import *
from gaugeRnR import *
from data import data
import pprint

g = GaugeRnR(data.shape)
g.calculate(data)
#pprint.pprint(g.Var)
#pprint.pprint(g.F)
pprint.pprint(g.P)