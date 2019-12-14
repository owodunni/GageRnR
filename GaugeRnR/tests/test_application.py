import unittest
from GaugeRnR import main


class MainTest(unittest.TestCase):
    def test_FileNotFoundError(self):
        self.assertRaises(
            FileNotFoundError,
            main,
            ['-f', "giberishFile.csv",
             "-s", "3,5,11"])

    def test_StructureToManyArguments(self):
        self.assertRaises(
            AttributeError,
            main,
            ['-f', "data/data_mXop.csv",
             "-s", "3,5,11,12"])

    def test_StructureNegativeArguments(self):
        self.assertRaises(
            AttributeError,
            main,
            ['-f', "data/data_mXop.csv",
             "-s", "-3,5,11"])

    def test_OkArguments(self):
        main(['-f', "data/data_mXop.csv",
              '-s', "3,5,11"])
        self.assertTrue(True)

    def test_AxesToManyArguments(self):
        self.assertRaises(
            AttributeError,
            main,
            ['-f', "data/data_mXop.csv",
             "-s", "3,5,11",
             "-a", "3,5,11,3"])

    def test_AxesNegativeArguments(self):
        self.assertRaises(
            AttributeError,
            main,
            ['-f', "data/data_mXop.csv",
             "-s", "3,5,11",
             "-a", "3,5,-11"])

    def test_OkAxesArguments(self):
        main(['-f', "data/data_mXop.csv",
              "-s", "3,5,11",
              "-a", "0,1,2"])
        self.assertTrue(True)

    def test_DifferentAxes(self):
        main(['-f', "data/data_demoGRnR.csv",
              "-s", "3,10,3",
              "-a", "0,2,1"])
        self.assertTrue(True)
