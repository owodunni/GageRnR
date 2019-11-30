#!/usr/bin/env python3
import unittest
from stats import *

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

if __name__ == '__main__':
    unittest.main()