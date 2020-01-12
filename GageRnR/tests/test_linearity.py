import unittest
from GageRnR import Linearity, Component
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
        np.testing.assert_array_almost_equal(
            P[Component.TOTAL],
            1, 3)

    def test_LinearityGt(self):
        n = Linearity(linearityData, partGt=np.array([0, 1]))
        K, Bias, P = n.calculateLinearity()

        np.testing.assert_array_almost_equal(
            K[Component.TOTAL],
            1, 3)
        np.testing.assert_array_almost_equal(
            Bias[Component.TOTAL],
            0, 3)
        np.testing.assert_array_almost_equal(
            P[Component.TOTAL],
            0.209, 3)

    def test_EstimateCoef(self):
        n = Linearity(data)
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])
        K, Bias, P = n.estimateCoef(x, y)

        np.testing.assert_array_almost_equal(
            K,
            1.16969, 3)
        np.testing.assert_array_almost_equal(
            Bias,
            1.236, 3)
        np.testing.assert_array_almost_equal(
            P,
            0, 3)

    def test_EstimateCoefOffset(self):
        n = Linearity(data)
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        K, Bias, P = n.estimateCoef(x, y)

        np.testing.assert_array_almost_equal(
            K,
            1, 3)
        np.testing.assert_array_almost_equal(
            Bias,
            1, 3)
        np.testing.assert_array_almost_equal(
            P,
            0, 3)

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
