#!/usr/bin/env python3
"""The GaugeRnR Tests."""
import unittest
from GaugeRnR import Statistics, Component, Result
from .data import data, squaresMeas
import numpy as np


class TestStatistics(unittest.TestCase):
    """The Statistics Tests."""

    def test_stdShape(self):
        g = Statistics(data)
        std = g.calculateStd()

        self.assertEqual(std[Component.TOTAL].size,1)
        self.assertEqual(std[Component.OPERATOR].shape,(3,))
        self.assertEqual(std[Component.PART].shape,(5,))
    
    def test_std(self):
        g = Statistics(data)
        std = g.calculateStd()

        stdPart0 = np.std(data[:,0,:], ddof=1)
        stdOperator0 = np.std(data[0,:,:], ddof=1)
        self.assertEqual(stdOperator0, std[Component.OPERATOR][0])
        self.assertEqual(stdPart0, std[Component.PART][0])