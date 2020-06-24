import unittest
from GageRnR import main
import os


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

    def test_GenerateReport(self):
        main(['-f', "data/data_demoGRnR.csv",
              "-s", "3,10,3",
              "-a", "0,2,1",
              "-o", 'build'])
        self.assertTrue(os.path.exists('build/index.html'))
        self.assertTrue(os.path.exists('build/Operators Box Plot.html'))
        self.assertTrue(os.path.exists('build/Parts Box Plot.html'))
        self.assertFalse(os.path.exists('build/Residual Linearity Plot.html'))
        self.assertTrue(os.path.exists('build/bootstrap.min.css'))

    def test_GenerateReportInNewFolder(self):
        main(['-f', "data/data_demoGRnR.csv",
              "-s", "3,10,3",
              "-a", "0,2,1",
              "-o", 'build/report'])
        self.assertTrue(os.path.exists('build/report/index.html'))
        self.assertTrue(os.path.exists('build/report/Operators Box Plot.html'))
        self.assertTrue(os.path.exists('build/report/Parts Box Plot.html'))
        self.assertFalse(os.path.exists('build/report/Residual Linearity Plot.html'))
        self.assertTrue(os.path.exists('build/report/bootstrap.min.css'))

    def test_GenerateReportWithGt(self):
        main(['-f', "data/data_demoGRnR.csv",
              "-s", "3,10,3",
              "-a", "0,2,1",
              "-o", 'build/gtReport',
              "-g", "40,42,30,43,29,45,27.5,42,26,35"])
        self.assertTrue(os.path.exists('build/gtReport/index.html'))
        self.assertTrue(os.path.exists('build/gtReport/Operators Box Plot.html'))
        self.assertTrue(os.path.exists('build/gtReport/Parts Box Plot.html'))
        self.assertTrue(os.path.exists('build/gtReport/Residual Linearity Plot.html'))
        self.assertTrue(os.path.exists('build/gtReport/bootstrap.min.css'))

    def test_FailToGenerateReport(self):
        forbiddenFolders = {'nt': "COM1", 'posix': "/build"}
        self.assertRaises(
            Exception,
            main, [
                '-f', "data/data_demoGRnR.csv",
                "-s", "3,10,3",
                "-a", "0,2,1",
                "-o", forbiddenFolders[os.name]])
