#!/usr/bin/env python3
"""Example showing how to use GageRnR."""
from math import sqrt
from GageRnR import Distribution, Settings, Generator
from GageRnR import GageRnR
import numpy as np

sigmaOp = 0.5
sigmaP = 5
sigmaPOP = 0.1
sigmaMeas = 1

numbO = 5
numbP = 7
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
    measurements=measurements)

gen = Generator(settings)
g = GageRnR(gen.data)
g.calculate()
print(g.summary())

np.savetxt('data/data_opXm.csv', gen.data.reshape(numbMeas, numbO*numbP), delimiter=';')
