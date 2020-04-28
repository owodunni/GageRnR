#!/usr/bin/env python3
import unittest
from GageRnR import DataLoader


class TestDataLoader(unittest.TestCase):

    def test_LoadData(self):

        loader = DataLoader()
        data = loader.load(
            file="data/data_demoGRnR.csv",
            structure=[3, 10, 3],
            axes=[0, 2, 1],
            delimiter=',')
        self.assertEqual(data.shape, (3, 10, 3))
