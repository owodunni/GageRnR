#!/usr/bin/env python3
from generator import *
from stats import *

operator = Distribution(2,0,0.1)
parts = Distribution(3,10,0)
measurements = Distribution(5000,0,0.5)

settings = Settings(
    operators=operator,
    parts=parts,
    measurments=measurements)

generator = Generator(settings)

stats = GaugeRnR(
    operators=operator.number,
    parts=parts.number,
    measurements=measurements.number,
    data=generator.data)
