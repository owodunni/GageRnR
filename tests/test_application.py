import unittest
from context import main


class MainTest(unittest.TestCase):
    def test_main(self):
        main(['-v'])
