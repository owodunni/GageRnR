#!/usr/bin/env python3
from generator import *

operator = Distribution(2,0,0.1)
parts = Distribution(3,10,1)
measurements = Distribution(5,0,0.1)

settings = Settings(
    operators=operator,
    parts=parts,
    measurments=measurements)

generator = Generator(settings)

print(generator.data.shape)