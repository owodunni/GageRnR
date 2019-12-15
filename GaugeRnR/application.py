"""GaugeRnR.

Usage:
    GaugeRnR -f FILE -s STRUCTURE [-a <AXES>] [-d <DELIMITER>] [-o <FOLDER>]
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
    -o --output=<FOLDER> Report output directory
    -g --groundTruth=<PARTS> Ground Truth data for parts
    -h --help     Show this screen.
    -v --version  Show version.
"""
from docopt import docopt
import os.path

import GaugeRnR
from .reportGenerator import ReportGenerator


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
        print(arguments)
        self.file = str(arguments["--file"])
        self.structure = toInt(arguments["--structure"])
        self.axes = toInt(arguments["--axes"])
        self.delimiter = str(arguments["--delimiter"])
        if("--output" in arguments):
            self.outputFolder = arguments["--output"]

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

        s = GaugeRnR.Statistics(data)
        s.calculate()

        if not hasattr(self, 'outputFolder'):
            return
        
        rg = ReportGenerator(self.outputFolder)
        rg.addTitle(s.title)
        rg.addTable(s.summary(tableFormat="html"))
        rg.addPlot(s.creatPartsBoxPlot(), 'partsBoxPlot')
        rg.generateReport()


        
        
        #fig = s.creatOperatorsBoxPlot()
        #fig.show()
        #fig = s.creatPartsBoxPlot()
        #fig.show()
        #fig = s.create3DPlot()
        #fig.show()
