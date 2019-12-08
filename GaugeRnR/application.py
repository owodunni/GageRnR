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


class Application():

    def __init__(self, argv=None):
        arguments = docopt(__doc__, argv)
        print(arguments)

    def run(self):
        print("running")
