from enum import Enum
import numpy as np


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


class Statistics(object):
    def __init__(self, data):
        self.data = data
        self.parts = data.shape[1]
        self.operators = data.shape[0]
        self.measurements = data.shape[2]

    def calculateMean(self):
        """Calculate Mean."""
        mu = np.mean(self.data)

        omu = np.mean(self.data, axis=1)
        omu = np.mean(omu, axis=1)

        pmu = np.mean(self.data, axis=0)
        pmu = np.mean(pmu, axis=1)

        emu = np.mean(self.data, axis=2)
        emu = emu.reshape(self.parts * self.operators)

        return {
            Component.TOTAL: mu,
            Component.OPERATOR: omu,
            Component.PART: pmu,
            Component.MEASUREMENT: emu}

    def calculateStd(self):
        std = np.std(self.data, ddof=1)
        stdo = np.std(
            self.data.reshape(
                self.operators,
                self.measurements*self.parts),
            axis=1,
            ddof=1)
        data = np.transpose(self.data, axes=(1, 0, 2))
        stdp = np.std(
            data.reshape(
                self.parts,
                self.measurements*self.operators),
            axis=1,
            ddof=1)
        return {
            Component.TOTAL: std,
            Component.OPERATOR: stdo,
            Component.PART: stdp
        }
