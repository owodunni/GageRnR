from enum import Enum

class Statistics():
    """Analys mean, std and if the data is gaussian."""

    def __init(self, data):
        """Initialize Statistics algorithm.

        :param numpy.array data:
            The data tha we want to analyse using GaugeRnR.
            The input should be structeted in a 3d array
            n[i,j,k] where i = operator, j = part, k = measurement
        """
        self.data = data
        self.parts = data.shape[1]
        self.operators = data.shape[0]
        self.measurements = data.shape[2]

    class Component(Enum):
        """Enum containing the different Variance parts of GaugeRnR."""

        OPERATOR = 0
        PART = 1
        OPERATOR_BY_PART = 2
        MEASUREMENT = 3
        TOTAL = 4


    ComponentNames = {
        Component.OPERATOR: 'Operator',
        Component.PART: 'Part',
        Component.OPERATOR_BY_PART: 'Operator by Part',
        Component.MEASUREMENT: 'Measurment',
        Component.TOTAL: 'Total'}

    ComponentNames = {
        Component.OPERATOR: 'Operator',
        Component.PART: 'Part',
        Component.OPERATOR_BY_PART: 'Operator by Part',
        Component.MEASUREMENT: 'Measurment',
        Component.TOTAL: 'Total'}


    class Result(Enum):
        """Enum containing the measurements calculated by GaugeRnR."""

        DF = 0
        Mean = 1
        SS = 3
        MS = 4
        Var = 5
        Std = 6
        F = 7
        P = 8


    ResultNames = {
        Result.DF: 'DF',
        Result.SS: 'SS',
        Result.MS: 'MS',
        Result.Var: 'Var (\u03C3\u00B2)',
        Result.Std: 'Std (\u03C3)',
        Result.F: 'F-value',
        Result.P: 'P-value'}
