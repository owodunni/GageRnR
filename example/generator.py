#!/usr/bin/env python3
"""Example showing how to use generate gauge RnR data."""
from math import sqrt
from context import Distribution, Settings, Generator
from context import GaugeRnR
from numpy import savetxt

sigmaOp = 0.5
sigmaP = 5
sigmaPOP = 0.1
sigmaMeas = 1

numbO = 3
numbP = 5
numbMeas = 11

print("sigmaTot: ", sqrt(sigmaOp**2 + sigmaP**2 + sigmaMeas**2 + sigmaPOP**2))

operator = Distribution(numbO, 0, sigmaOp)
parts = Distribution(numbP, 100, sigmaP)
partOperator = Distribution(numbO*numbP, 0, sigmaOp)
measurements = Distribution(numbMeas, 0, sigmaMeas)

settings = Settings(
    operators=operator,
    parts=parts,
    partOperator=partOperator,
    measurments=measurements)

gen = Generator(settings)
g = GaugeRnR(gen.data)
g.calculate()
print(g.summary())

savetxt('data/data_mXop.csv', gen.data.reshape(numbMeas, numbO*numbP), delimiter=';')
