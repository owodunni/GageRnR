#!/usr/bin/env python3
"""The GageRnR Tests."""
import unittest
from GageRnR import GageRnR, Component, Result
from .data import data, squaresMeas
import numpy as np


class TestGageRnR(unittest.TestCase):
    """The GageRnR Tests."""

    def test_setupShape(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        self.assertEqual(g.operators, 3)
        self.assertEqual(g.parts, 5)
        self.assertEqual(g.measurements, 3)

    def test_calculateDoF(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        dof = g.calculateDoF()
        self.assertEqual(dof[Component.OPERATOR], 2)
        self.assertEqual(dof[Component.PART], 4)
        self.assertEqual(dof[Component.OPERATOR_BY_PART], 8)
        self.assertEqual(dof[Component.MEASUREMENT], 30)
        self.assertEqual(dof[Component.TOTAL], 44)

    def test_calculateMean(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        mean = g.calculateMean()

        np.testing.assert_array_almost_equal(
            mean[Component.TOTAL], [2.9437], 3)

        np.testing.assert_array_almost_equal(
            mean[Component.OPERATOR], [3.1567, 2.98, 2.6947], 3)

        np.testing.assert_array_almost_equal(
            mean[Component.PART],
            [3.1689, 2.1489, 4.0989, 3.3667, 1.9356], 3)

        np.testing.assert_array_almost_equal(
            mean[Component.MEASUREMENT],
            [3.447, 2.393, 4.260, 3.537, 2.147,
             3.133, 2.210, 4.157, 3.413, 1.987,
             2.927, 1.843, 3.880, 3.150, 1.673], 3)

    def test_calculateSquares(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        squares = g.calculateSquares()

        np.testing.assert_array_almost_equal(
            squares[Component.OPERATOR],
            [0.0453, 0.0013, 0.0621], 3)

        np.testing.assert_array_almost_equal(
            squares[Component.PART],
            [0.0507, 0.6318, 1.3343, 0.1788, 1.0165], 3)

        np.testing.assert_array_almost_equal(
            squares[Component.MEASUREMENT],
            squaresMeas, 3)

    def test_calculateSumOfDeviations(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        SD = g.calculateSumOfDeviations()

        self.assertAlmostEqual(
            SD[Component.TOTAL], 32.317, 3)

        self.assertAlmostEqual(
            SD[Component.OPERATOR], 0.1087, 3)

        self.assertAlmostEqual(
            SD[Component.PART], 3.2122, 3)

        self.assertAlmostEqual(
            SD[Component.MEASUREMENT], 1.712, 3)

    def test_calculateSS(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        SS = g.calculateSS()

        self.assertAlmostEqual(
            SS[Component.TOTAL], 32.317, 3)

        self.assertAlmostEqual(
            SS[Component.OPERATOR], 1.630, 3)

        self.assertAlmostEqual(
            SS[Component.PART], 28.909, 3)

        self.assertAlmostEqual(
            SS[Component.OPERATOR_BY_PART], 0.065, 3)

        self.assertAlmostEqual(
            SS[Component.MEASUREMENT], 1.712, 3)

    def test_calculateMS(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        MS = g.result[Result.MS]

        self.assertAlmostEqual(
            MS[Component.OPERATOR], 0.815, 3)
        self.assertAlmostEqual(
            MS[Component.PART], 7.227, 3)
        self.assertAlmostEqual(
            MS[Component.OPERATOR_BY_PART], 0.008, 3)
        self.assertAlmostEqual(
            MS[Component.MEASUREMENT], 0.057, 3)

    def test_calculateVar(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        Var = g.result[Result.Var]

        self.assertAlmostEqual(
            Var[Component.TOTAL], 0.9130, 3)
        self.assertAlmostEqual(
            Var[Component.OPERATOR], 0.0538, 3)
        self.assertAlmostEqual(
            Var[Component.PART], 0.8021, 3)
        self.assertAlmostEqual(
            Var[Component.OPERATOR_BY_PART], 0, 3)
        self.assertAlmostEqual(
            Var[Component.MEASUREMENT], 0.057, 3)

    def test_calculateF(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        F = g.result[Result.F]

        self.assertAlmostEqual(
            F[Component.OPERATOR], 100.322, 3)
        self.assertAlmostEqual(
            F[Component.PART], 889.458, 3)
        self.assertAlmostEqual(
            F[Component.OPERATOR_BY_PART], 0.142, 3)

    def test_calculateP(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        P = g.result[Result.P]

        self.assertAlmostEqual(
            P[Component.OPERATOR], 0, 3)
        self.assertAlmostEqual(
            P[Component.PART], 0, 3)
        self.assertAlmostEqual(
            P[Component.OPERATOR_BY_PART], 0.9964, 4)

    def test_str(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.__str__()
        self.assertTrue(True)

    def test_strAfterCalculated(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        g.__str__()
        self.assertTrue(True)

    def test_summaryException(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        self.assertRaises(Exception, g.summary)

    def test_summary(self):
        """The GageRnR Tests."""
        g = GageRnR(data)
        g.calculate()
        g.summary()
        self.assertTrue(True)
