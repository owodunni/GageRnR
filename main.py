#!/usr/bin/env python3
from generator import *
from stats import *

sigmaOp = 0.1
sigmaP = 0
sigmaPOP = 0.1
sigmaMeas = 0.5

numbO = 100
numbP = 3
numbMeas = 100

print("sigmaTot: ", sqrt(sigmaOp**2 + sigmaP**2 + sigmaMeas**2 + sigmaPOP**2))

operator = Distribution(numbO,0,sigmaOp)
parts = Distribution(numbP,10,sigmaP)
partOperator = Distribution(numbO*numbP,0,sigmaOp)
measurements = Distribution(numbMeas,0,sigmaMeas)

settings = Settings(
    operators=operator,
    parts=parts,
    partOperator=partOperator,
    measurments=measurements)

generator = Generator(settings)

stats = GaugeRnR(
    operators=operator.number,
    parts=parts.number,
    measurements=measurements.number,
    data=generator.data)
