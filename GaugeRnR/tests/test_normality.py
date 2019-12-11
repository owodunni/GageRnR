import unittest
from GaugeRnR import Normality, Component
from .data import data
import numpy as np

class TestStatistics(unittest.TestCase):
    """The Statistics Tests."""

    def test_normalityShape(self):
        n = Normality(data)
        W, P = n.calculateNormality()

        self.assertEqual(P[Component.TOTAL].size, 1)
        self.assertEqual(P[Component.OPERATOR].shape, (3,))
        self.assertEqual(P[Component.PART].shape, (5,))
        self.assertEqual(W[Component.TOTAL].size, 1)
        self.assertEqual(W[Component.OPERATOR].shape, (3,))
        self.assertEqual(W[Component.PART].shape, (5,))

    def test_normality(self):
        n = Normality(data)
        W, P = n.calculateNormality()

        np.testing.assert_array_almost_equal(
            P[Component.TOTAL],
            [0.05104245], 3)
        np.testing.assert_array_almost_equal(
            P[Component.OPERATOR],
            [0.063, 0.301, 0.15], 3)
        np.testing.assert_array_almost_equal(
            P[Component.PART],
            [0.714, 0.273, 0.387, 0.231, 0.728], 3)
        np.testing.assert_array_almost_equal(
            W[Component.TOTAL],
            [0.95], 3)
        np.testing.assert_array_almost_equal(
            W[Component.OPERATOR],
            [0.888, 0.933, 0.913], 3)
        np.testing.assert_array_almost_equal(
            W[Component.PART],
            [0.952, 0.904, 0.919, 0.896, 0.953], 3)

    def test_str(self):
        n = Normality(data)
        n.__str__()
        self.assertTrue(True)

    def test_strAfterCalculated(self):
        n = Normality(data)
        n.calculate()
        n.__str__()
        self.assertTrue(True)

    def test_summaryException(self):
        n = Normality(data)
        self.assertRaises(Exception, n.summary)

    def test_summary(self):
        n = Normality(data)
        n.calculate()
        n.summary()
        self.assertTrue(True)
