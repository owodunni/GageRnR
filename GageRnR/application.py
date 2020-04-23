"""GageRnR.

The input data should be structured
in a 3d array n[i,j,k] where
i = operator, j = part, k = measurement
Stored to file this data would look:
m1    m2    m3
3.29; 3.41; 3.64  # p1 | o1
2.44; 2.32; 2.42  # p2
3.08; 3.25; 3.07  # p1 | o2
2.53; 1.78; 2.32  # p2
3.04; 2.89; 2.85  # p1 | o3
1.62; 1.87; 2.04  # p2

More info: https://github.com/owodunni/GageRnR

Usage:
    GageRnR -f FILE -s STRUCTURE [-a <AXES>] [-d <DELIMITER>] [-o <FOLDER>] [-g <PARTS>]
    GageRnR -h | --help
    GageRnR -v | --version

Examples:
    GageRnR -f data.csv -s5,7,11 -o report
    GageRnR -f data/data_mXop.csv -s 3,5,11 -o outDir
    GageRnR -f data/data_opXm.csv -s 5,7,11 -a 2,1,0 -o outDir
    GageRnR -f data/data_demoGRnR.csv -s 3,10,3 -a 0,2,1 -g 40,42,30,43,29,45,27.5,42,26,35 -o outDir

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

import GageRnR
from .reportGenerator import ReportGenerator


def toInt(values):
    return [int(v) for v in values.split(',')]


def toFloat(values):
    return [float(v) for v in values.split(',')]


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
        arguments = docopt(__doc__, argv, version=GageRnR.__version__)
        self.file = str(arguments["--file"])
        self.structure = toInt(arguments["--structure"])
        self.axes = toInt(arguments["--axes"])
        self.delimiter = str(arguments["--delimiter"])

        if(arguments["--groundTruth"] is not None):
            self.gt = toFloat(arguments["--groundTruth"])

        if(arguments["--output"] is not None):
            self.outputFolder = arguments["--output"]

    def check(self):
        if not os.path.isfile(self.file):
            raise FileNotFoundError(self.file)
        checkIntegerList("Strucuture", self.structure, 1)
        checkIntegerList("Axes", self.axes)

    def run(self):
        loader = GageRnR.DataLoader()
        data = loader.load(
            file=self.file,
            structure=self.structure,
            axes=self.axes,
            delimiter=self.delimiter)

        g = GageRnR.GageRnR(data)
        g.calculate()

        s = GageRnR.Statistics(data)
        s.calculate()

        n = GageRnR.Normality(data)
        n.calculate()

        if hasattr(self, 'gt'):
            lin = GageRnR.Linearity(data=data, partGt=self.gt)
            lin.calculate()

        if not hasattr(self, 'outputFolder'):
            return

        rg = ReportGenerator(self.outputFolder)

        rg.addTitle(g.title)
        rg.addDoc(g)
        rg.addTable(g.summary(tableFormat="html"))

        rg.addTitle(s.title)
        rg.addDoc(s)
        rg.addTable(s.summary(tableFormat="html"))
        rg.addPlot(s.creatPartsBoxPlot(), 'Parts Box Plot')
        rg.addPlot(s.creatOperatorsBoxPlot(), 'Operators Box Plot')

        rg.addTitle(n.title)
        rg.addDoc(n)
        rg.addTable(n.summary(tableFormat="html"))

        if hasattr(self, 'gt'):
            rg.addTitle(lin.title)
            rg.addDoc(lin)
            rg.addTable(lin.summary(tableFormat="html"))
            rg.addPlot(lin.creatLinearityPlot(), 'Residual Linearity Plot')

        rg.generateReport()

        print("Report writen to: " + self.outputFolder)
