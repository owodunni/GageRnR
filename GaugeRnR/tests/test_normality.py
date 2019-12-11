import unittest
from GaugeRnR import Normality, Component
from .data import data
import numpy as np

class TestStatistics(unittest.TestCase):
    """The Statistics Tests."""

    def test_normalityShape(self):
        n = Normality(data)
        #W, P = n.calculateNormality()

        #self.assertEqual(P[Component.TOTAL].size, 1)
        #self.assertEqual(P[Component.OPERATOR].shape, (3,))
        #self.assertEqual(P[Component.PART].shape, (5,))
        #self.assertEqual(W[Component.TOTAL].size, 1)
        #self.assertEqual(W[Component.OPERATOR].shape, (3,))
        #self.assertEqual(W[Component.PART].shape, (5,))
