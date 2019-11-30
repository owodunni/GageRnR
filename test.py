#!/usr/bin/env python3
import unittest
from stats import *

class TestStats(unittest.TestCase):

    def test_setupShape(self):
        g = GaugeRnR([3, 5, 3])
        self.assertEqual(g.operators, 3)
        self.assertEqual(g.parts, 5)
        self.assertEqual(g.measurements, 3)

if __name__ == '__main__':
    unittest.main()