#!/usr/bin/env python3
"""The GageRnR Tests."""
import unittest
from GageRnR import Distribution, Settings, Generator
from GageRnR import GageRnR, Component, Result
from math import sqrt
from numpy.random import seed


class TestGageRnR(unittest.TestCase):
    """The GageRnR Tests."""

    def setUp(self):
        self.sigmaOp = 0.5
        self.sigmaP = 5
        self.sigmaPOP = 0.1
        self.sigmaMeas = 1

        numbO = 3
        numbP = 400
        numbMeas = 100

        operator = Distribution(numbO, 0, self.sigmaOp)
        parts = Distribution(numbP, 100, self.sigmaP)
        partOperator = Distribution(numbO*numbP, 0, self.sigmaOp)
        measurements = Distribution(numbMeas, 0, self.sigmaMeas)

        settings = Settings(
            operators=operator,
            parts=parts,
            partOperator=partOperator,
            measurments=measurements)

        seed(1)
        self.gen = Generator(settings)

    def test_generatorTotalStd(self):
        """The GageRnR Tests."""

        g = GageRnR(self.gen.data)
        g.calculate()

        sigmaTot = sqrt(self.sigmaOp**2 + self.sigmaP**2 + self.sigmaMeas**2 + self.sigmaPOP**2)
        sigmaEst = g.result[Result.Std][Component.TOTAL]
        self.assertLess(sigmaTot - sigmaEst, 0.1)
