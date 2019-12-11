"""GaugeRnR.

Usage:
    GaugeRnR -f FILE -s STRUCTURE [-a <AXES>] [-d <DELIMITER>]
    GaugeRnR -h | --help
    GaugeRnR -v | --version

Examples:
    GaugeRnR -f data.csv -s5,7,11
    GaugeRnR -f data.csv -s5,7,11 --a 1,0,2 --d ,

Options:
    -f --file=FILE Load input data.
    -s --structure=STRUCTURE Data structure.
        Order should be operators, parts, measurements.
    -a --axes=<AXES>  Order of data axes [default: 0,1,2].
    -d --delimiter=<DELIMITER>  Order of data axes [default: ;].
    -h --help     Show this screen.
    -v --version  Show version.
"""
from docopt import docopt
import os.path

import GaugeRnR


def toInt(values):
    return [int(s) for s in values.split(',')]


def positiveIntegers(values, minValue):
    for value in values:
        if value < minValue:
            return False
    return True


def checkIntegerList(name, values, minValue=0):
    if(len(values) != 3):
        raise AttributeError(name, " can only have three values.")
    if(not positiveIntegers(values, minValue)):
        raise AttributeError(name, " can only be positive integers.")


class Application():

    def __init__(self, argv=None):
        arguments = docopt(__doc__, argv, version=GaugeRnR.__version__)
        self.file = str(arguments["--file"])
        self.structure = toInt(arguments["--structure"])
        self.axes = toInt(arguments["--axes"])
        self.delimiter = str(arguments["--delimiter"])

    def check(self):
        if not os.path.isfile(self.file):
            raise FileNotFoundError(self.file)
        checkIntegerList("Strucuture", self.structure, 1)
        checkIntegerList("Axes", self.axes)

    def run(self):
        loader = GaugeRnR.DataLoader()
        data = loader.load(
            file=self.file,
            structure=self.structure,
            axes=self.axes,
            delimiter=self.delimiter)
        g = GaugeRnR.GaugeRnR(data)
        g.calculate()
        print(g)
        s = GaugeRnR.Statistics(data)
        s.calculate()
        print(s)
        n = GaugeRnR.Normality(data)
        n.calculate()
        print(n)
