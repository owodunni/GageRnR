import unittest
from context import main


class MainTest(unittest.TestCase):
    def test_main(self):
        self.assertRaises(
            FileNotFoundError,
            main,
            ['-f', "giberishFile.csv",
             "-s", "3,5,11"])
