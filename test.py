#!/usr/bin/env python3
import unittest
from gaugeRnR import *
from data import *
import numpy as np
import pprint

class TestStats(unittest.TestCase):

    def test_setupShape(self):
        g = GaugeRnR([3, 5, 3])
        self.assertEqual(g.operators, 3)
        self.assertEqual(g.parts, 5)
        self.assertEqual(g.measurements, 3)

    def test_calculateDoF(self):
        g = GaugeRnR([3, 5, 3])
        dof = g.calculateDoF()
        self.assertEqual(dof[GaugeRnR.OPERATOR], 2)
        self.assertEqual(dof[GaugeRnR.PART], 4)
        self.assertEqual(dof[GaugeRnR.OPERATOR_BY_PART], 8)
        self.assertEqual(dof[GaugeRnR.MEASUREMENT], 30)
        self.assertEqual(dof[GaugeRnR.TOTAL], 44)

    def test_calculateMean(self):
        g = GaugeRnR(data.shape)
        mean = g.calculateMean(data)

        self.assertAlmostEqual(
            mean[GaugeRnR.TOTAL], 2.9437, 3)

        np.testing.assert_array_almost_equal(
            mean[GaugeRnR.OPERATOR], [3.1567, 2.98, 2.6947],3)

        np.testing.assert_array_almost_equal(
            mean[GaugeRnR.PART],
            [3.1689, 2.1489, 4.0989, 3.3667, 1.9356],3)

        np.testing.assert_array_almost_equal(
            mean[GaugeRnR.MEASUREMENT],
            [3.447, 2.393, 4.260, 3.537, 2.147,
            3.133, 2.210, 4.157, 3.413, 1.987,
            2.927, 1.843, 3.880, 3.150, 1.673],3)
    
    def test_calculateSquares(self):
        g = GaugeRnR(data.shape)
        squares = g.calculateSquares(data)

        np.testing.assert_array_almost_equal(
            squares[GaugeRnR.OPERATOR],
            [0.0453, 0.0013, 0.0621],3)

        np.testing.assert_array_almost_equal(
            squares[GaugeRnR.PART],
            [0.0507, 0.6318, 1.3343, 0.1788, 1.0165],3)

        np.testing.assert_array_almost_equal(
            squares[GaugeRnR.MEASUREMENT],
            squaresMeas,3)


    def test_calculateSumOfDeviations(self):
        g = GaugeRnR(data.shape)
        SD = g.calculateSumOfDeviations(data)

        self.assertAlmostEqual(
            SD[GaugeRnR.TOTAL], 32.317, 3)
        
        self.assertAlmostEqual(
            SD[GaugeRnR.OPERATOR], 0.1087, 3)

        self.assertAlmostEqual(
            SD[GaugeRnR.PART], 3.2122, 3)

        self.assertAlmostEqual(
            SD[GaugeRnR.MEASUREMENT], 1.712, 3)

    def test_calculateSS(self):
        g = GaugeRnR(data.shape)
        SS = g.calculateSS(data)

        self.assertAlmostEqual(
            SS[GaugeRnR.TOTAL], 32.317, 3)

        self.assertAlmostEqual(
            SS[GaugeRnR.OPERATOR], 1.630, 3)

        self.assertAlmostEqual(
            SS[GaugeRnR.PART], 28.909, 3)

        self.assertAlmostEqual(
            SS[GaugeRnR.OPERATOR_BY_PART], 0.065, 3)

        self.assertAlmostEqual(
            SS[GaugeRnR.MEASUREMENT], 1.712, 3)

    def test_calculateMS(self):
        g = GaugeRnR(data.shape)
        g.calculate(data)

        self.assertAlmostEqual(
            g.MS[GaugeRnR.OPERATOR], 0.815, 3)
        self.assertAlmostEqual(
            g.MS[GaugeRnR.PART], 7.227, 3)
        self.assertAlmostEqual(
            g.MS[GaugeRnR.OPERATOR_BY_PART], 0.008, 3)
        self.assertAlmostEqual(
            g.MS[GaugeRnR.MEASUREMENT], 0.057, 3)
    
    def test_calculateF(self):
        g = GaugeRnR(data.shape)
        g.calculate(data)

        self.assertAlmostEqual(
            g.F[GaugeRnR.OPERATOR], 100.322, 3)
        self.assertAlmostEqual(
            g.F[GaugeRnR.PART], 889.458, 3)
        self.assertAlmostEqual(
            g.F[GaugeRnR.OPERATOR_BY_PART], 0.142, 3)

    def test_calculateP(self):
        g = GaugeRnR(data.shape)
        g.calculate(data)

        self.assertAlmostEqual(
            g.P[GaugeRnR.OPERATOR], 0, 3)
        self.assertAlmostEqual(
            g.P[GaugeRnR.PART], 0, 3)
        self.assertAlmostEqual(
            g.P[GaugeRnR.OPERATOR_BY_PART], 0.9964, 4)

if __name__ == '__main__':
    unittest.main()
