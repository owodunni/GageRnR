#!/usr/bin/env python3
"""The GaugeRnR Tests."""
import unittest
from context import GaugeRnR
from context import Statistics as st
from data import data, squaresMeas
import numpy as np


class TestGaugeRnR(unittest.TestCase):
    """The GaugeRnR Tests."""

    def test_setupShape(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        self.assertEqual(g.operators, 3)
        self.assertEqual(g.parts, 5)
        self.assertEqual(g.measurements, 3)

    def test_calculateDoF(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        dof = g.calculateDoF()
        self.assertEqual(dof[st.Component.OPERATOR], 2)
        self.assertEqual(dof[st.Component.PART], 4)
        self.assertEqual(dof[st.Component.OPERATOR_BY_PART], 8)
        self.assertEqual(dof[st.Component.MEASUREMENT], 30)
        self.assertEqual(dof[st.Component.TOTAL], 44)

    def test_calculateMean(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        mean = g.calculateMean()

        self.assertAlmostEqual(
            mean[st.Component.TOTAL], 2.9437, 3)

        np.testing.assert_array_almost_equal(
            mean[st.Component.OPERATOR], [3.1567, 2.98, 2.6947], 3)

        np.testing.assert_array_almost_equal(
            mean[st.Component.PART],
            [3.1689, 2.1489, 4.0989, 3.3667, 1.9356], 3)

        np.testing.assert_array_almost_equal(
            mean[st.Component.MEASUREMENT],
            [3.447, 2.393, 4.260, 3.537, 2.147,
             3.133, 2.210, 4.157, 3.413, 1.987,
             2.927, 1.843, 3.880, 3.150, 1.673], 3)

    def test_calculateSquares(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        squares = g.calculateSquares()

        np.testing.assert_array_almost_equal(
            squares[st.Component.OPERATOR],
            [0.0453, 0.0013, 0.0621], 3)

        np.testing.assert_array_almost_equal(
            squares[st.Component.PART],
            [0.0507, 0.6318, 1.3343, 0.1788, 1.0165], 3)

        np.testing.assert_array_almost_equal(
            squares[st.Component.MEASUREMENT],
            squaresMeas, 3)

    def test_calculateSumOfDeviations(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        SD = g.calculateSumOfDeviations()

        self.assertAlmostEqual(
            SD[st.Component.TOTAL], 32.317, 3)

        self.assertAlmostEqual(
            SD[st.Component.OPERATOR], 0.1087, 3)

        self.assertAlmostEqual(
            SD[st.Component.PART], 3.2122, 3)

        self.assertAlmostEqual(
            SD[st.Component.MEASUREMENT], 1.712, 3)

    def test_calculateSS(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        SS = g.calculateSS()

        self.assertAlmostEqual(
            SS[st.Component.TOTAL], 32.317, 3)

        self.assertAlmostEqual(
            SS[st.Component.OPERATOR], 1.630, 3)

        self.assertAlmostEqual(
            SS[st.Component.PART], 28.909, 3)

        self.assertAlmostEqual(
            SS[st.Component.OPERATOR_BY_PART], 0.065, 3)

        self.assertAlmostEqual(
            SS[st.Component.MEASUREMENT], 1.712, 3)

    def test_calculateMS(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        MS = g.result[st.Result.MS]

        self.assertAlmostEqual(
            MS[st.Component.OPERATOR], 0.815, 3)
        self.assertAlmostEqual(
            MS[st.Component.PART], 7.227, 3)
        self.assertAlmostEqual(
            MS[st.Component.OPERATOR_BY_PART], 0.008, 3)
        self.assertAlmostEqual(
            MS[st.Component.MEASUREMENT], 0.057, 3)

    def test_calculateVar(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        Var = g.result[st.Result.Var]

        self.assertAlmostEqual(
            Var[st.Component.TOTAL], 0.9130, 3)
        self.assertAlmostEqual(
            Var[st.Component.OPERATOR], 0.0538, 3)
        self.assertAlmostEqual(
            Var[st.Component.PART], 0.8021, 3)
        self.assertAlmostEqual(
            Var[st.Component.OPERATOR_BY_PART], 0, 3)
        self.assertAlmostEqual(
            Var[st.Component.MEASUREMENT], 0.057, 3)

    def test_calculateF(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        F = g.result[st.Result.F]

        self.assertAlmostEqual(
            F[st.Component.OPERATOR], 100.322, 3)
        self.assertAlmostEqual(
            F[st.Component.PART], 889.458, 3)
        self.assertAlmostEqual(
            F[st.Component.OPERATOR_BY_PART], 0.142, 3)

    def test_calculateP(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        P = g.result[st.Result.P]

        self.assertAlmostEqual(
            P[st.Component.OPERATOR], 0, 3)
        self.assertAlmostEqual(
            P[st.Component.PART], 0, 3)
        self.assertAlmostEqual(
            P[st.Component.OPERATOR_BY_PART], 0.9964, 4)

    def test_str(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.__str__()
        self.assertTrue(True)

    def test_strAfterCalculated(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        g.__str__()
        self.assertTrue(True)

    def test_summaryException(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        self.assertRaises(Exception, g.summary)

    def test_summary(self):
        """The GaugeRnR Tests."""
        g = GaugeRnR(data)
        g.calculate()
        g.summary()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
