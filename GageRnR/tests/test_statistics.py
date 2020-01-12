#!/usr/bin/env python3
"""The GageRnR Tests."""
import unittest
from GageRnR import Statistics, Component
from .data import data
import numpy as np


class TestStatistics(unittest.TestCase):
    """The Statistics Tests."""

    def test_meanShape(self):
        g = Statistics(data)
        mean = g.calculateMean()

        self.assertEqual(mean[Component.TOTAL].size, 1)
        self.assertEqual(mean[Component.OPERATOR].shape, (3,))
        self.assertEqual(mean[Component.PART].shape, (5,))

    def test_stdShape(self):
        g = Statistics(data)
        std = g.calculateStd()

        self.assertEqual(std[Component.TOTAL].size, 1)
        self.assertEqual(std[Component.OPERATOR].shape, (3,))
        self.assertEqual(std[Component.PART].shape, (5,))

    def test_std(self):
        g = Statistics(data)
        std = g.calculateStd()

        stdPart0 = np.std(data[:, 0, :], ddof=1)
        stdOperator0 = np.std(data[0, :, :], ddof=1)
        self.assertEqual(stdOperator0, std[Component.OPERATOR][0])
        self.assertEqual(stdPart0, std[Component.PART][0])

    def test_mean(self):
        g = Statistics(data)
        mean = g.calculateMean()

        meanPart0 = np.mean(data[:, 0, :])
        meanOperator0 = np.mean(data[0, :, :])
        self.assertAlmostEqual(meanOperator0, mean[Component.OPERATOR][0])
        self.assertAlmostEqual(meanPart0, mean[Component.PART][0])

    def test_summaryRaise(self):
        g = Statistics(data)
        mean = g.calculateMean()

        meanPart0 = np.mean(data[:, 0, :])
        meanOperator0 = np.mean(data[0, :, :])
        self.assertAlmostEqual(meanOperator0, mean[Component.OPERATOR][0])
        self.assertAlmostEqual(meanPart0, mean[Component.PART][0])

    def test_str(self):
        s = Statistics(data)
        s.__str__()
        self.assertTrue(True)

    def test_strAfterCalculated(self):
        s = Statistics(data)
        s.calculate()
        s.__str__()
        self.assertTrue(True)

    def test_summaryException(self):
        s = Statistics(data)
        self.assertRaises(Exception, s.summary)

    def test_summary(self):
        s = Statistics(data)
        s.calculate()
        s.summary()
        self.assertTrue(True)
