import unittest
from GaugeRnR import Linearity, Component
from .data import data, linearityData
import numpy as np


class TestLinearity(unittest.TestCase):
    """The Statistics Tests."""

    def test_Linearity(self):
        n = Linearity(data)
        K, Bias, P = n.calculateLinearity()

        np.testing.assert_array_almost_equal(
            K[Component.TOTAL],
            0, 3)
        np.testing.assert_array_almost_equal(
            Bias[Component.TOTAL],
            0, 3)

    def test_LinearityGt(self):
        n = Linearity(linearityData)
        K, Bias, P = n.calculateLinearity(partGt=np.array([0, 1]))

        self.assertAlmostEqual(K[Component.TOTAL], 1)
        self.assertAlmostEqual(Bias[Component.TOTAL], 0)

    def test_EstimateCoef(self):
        n = Linearity(data)
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])
        K, Bias = n.estimateCoef(x, y)

        self.assertAlmostEqual(K, 1.1696969696969697)
        self.assertAlmostEqual(Bias, 1.2363636363636363)

    def test_EstimateCoefOffset(self):
        n = Linearity(data)
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        K, Bias = n.estimateCoef(x, y)

        self.assertAlmostEqual(K, 1)
        self.assertAlmostEqual(Bias, 1)

    def test_str(self):
        n = Linearity(data)
        n.__str__()
        self.assertTrue(True)

    def test_strAfterCalculated(self):
        n = Linearity(data)
        n.calculate()
        n.__str__()
        self.assertTrue(True)

    def test_summaryException(self):
        n = Linearity(data)
        self.assertRaises(Exception, n.summary)

    def test_summary(self):
        n = Linearity(data)
        n.calculate()
        n.summary()
        self.assertTrue(True)
