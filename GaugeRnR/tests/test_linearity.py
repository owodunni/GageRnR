import unittest
from GaugeRnR import Linearity, Component
from .data import data
import numpy as np


class TestLinearity(unittest.TestCase):
    """The Statistics Tests."""

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
