"""Module containing the algorithm for GaugeRnR."""
import numpy as np
import math
import scipy.stats as stats
from tabulate import tabulate
from enum import Enum


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
    Std = 2
    SS = 3
    MS = 4
    GaugeVar = 5
    GaugeStd = 6
    F = 7
    P = 8


ResultNames = {
    Result.DF: 'DF',
    Result.SS: 'SS',
    Result.MS: 'MS',
    Result.GaugeVar: 'Var (\u03C3\u00B2)',
    Result.GaugeStd: 'Std (\u03C3)',
    Result.F: 'F-value',
    Result.P: 'P-value'}


class GaugeRnR:
    """Main class for calculating GaugeRnR."""

    GRR = 'GaugeRnR'

    def __init__(self, data):
        """Initialize GaugeRnR algorithm.

        :param numpy.array data:
            The data tha we want to analyse using GaugeRnR.
            The input should be structeted in a 3d array
            n[i,j,k] where i = operator, j = part, k = measurement
        """
        self.data = data
        self.parts = data.shape[1]
        self.operators = data.shape[0]
        self.measurements = data.shape[2]

    def __str__(self):
        """Enum containing the measurements calculated by GaugeRnR."""
        if not hasattr(self, 'result'):
            return 'Shape: ' + \
                str([self.operators, self.parts, self.measurements])
        return self.toTabulare()

    def toTabulare(self, tableFormat="fancy_grid", precision='.3f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'GaugeRnR.calcualte() should be run before calling toTabular()')

        headers = ['Sources of Variance']

        for key in ResultNames:
            headers.append(ResultNames[key])

        table = []
        for comp in Component:
            innerTable = [ComponentNames[comp]]
            for key in ResultNames:
                if comp in self.result[key]:
                    innerTable.append(
                        format(self.result[key][comp], precision))
                else:
                    innerTable.append('')

            table.append(innerTable)

        return tabulate(
            table,
            headers=headers,
            tablefmt=tableFormat)

    def calculate(self):
        """Calculate GaugeRnR."""
        self.result = dict()
        self.result[Result.DF] = self.calculateDoF()
        self.result[Result.Mean] = self.calculateMean()
        self.result[Result.Std] = self.calculateStd()
        self.result[Result.SS] = self.calculateSS()

        self.result[Result.MS] = self.calculateMS(
            self.result[Result.DF],
            self.result[Result.SS])

        self.result[Result.GaugeVar] = self.calculateGaugeVariance(
            self.result[Result.MS])

        self.result[Result.GaugeStd] = self.calculateGaugeStd(self.result[Result.GaugeVar])

        self.result[Result.F] = self.calculateF(self.result[Result.MS])

        self.result[Result.P] = self.calculateP(
            self.result[Result.DF],
            self.result[Result.F])

        return self.result

    def calculateDoF(self):
        """Calculate Degrees of freedom."""
        oDoF = self.operators - 1
        pDoF = self.parts - 1
        opDoF = (self.parts - 1) * (self.operators - 1)
        eDof = self.parts * self.operators * (self.measurements - 1)
        totDof = self.parts * self.operators * self.measurements - 1
        return {
            Component.OPERATOR: oDoF,
            Component.PART: pDoF,
            Component.OPERATOR_BY_PART: opDoF,
            Component.MEASUREMENT: eDof,
            Component.TOTAL: totDof}

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
        """Calculate Std."""
        stdTotal = np.std(self.data, ddof=1)
        stdPerOperator = np.std(
            self.data.reshape(
                self.operators,
                self.parts*self.measurements),
            axis=1,
            ddof=1)

        stdPerPart = np.std(
            self.data.reshape(
                self.parts,
                self.operators*self.measurements),
            axis=1,
            ddof=1)

        return {
            Component.TOTAL: stdTotal,
            Component.OPERATOR: stdPerOperator,
            Component.PART: stdPerPart}

    def calculateSquares(self):
        """Calculate Squares."""
        mean = self.calculateMean()
        tS = (self.data - mean[Component.TOTAL])**2
        oS = (mean[Component.OPERATOR] - mean[Component.TOTAL])**2
        pS = (mean[Component.PART] - mean[Component.TOTAL])**2

        dataE = self.data.reshape(
            self.operators * self.parts,
            self.measurements)
        meanMeas = np.repeat(mean[Component.MEASUREMENT], self.measurements)
        meanMeas = meanMeas.reshape(
            self.operators * self.parts,
            self.measurements)

        mS = (dataE - meanMeas)**2
        return {
            Component.TOTAL: tS,
            Component.OPERATOR: oS,
            Component.PART: pS,
            Component.MEASUREMENT: mS}

    def calculateSumOfDeviations(self):
        """Calculate Sum of Deviations."""
        squares = self.calculateSquares()
        SD = dict()
        for key in squares:
            SD[key] = np.sum(squares[key])
        return SD

    def calculateSS(self):
        """Calculate Sum of Squares."""
        SS = self.calculateSumOfDeviations()

        SS[Component.OPERATOR] = \
            self.parts * self.measurements * \
            SS[Component.OPERATOR]
        SS[Component.PART] = \
            self.operators * self.measurements * \
            SS[Component.PART]
        SS[Component.OPERATOR_BY_PART] = \
            SS[Component.TOTAL] - (
                SS[Component.OPERATOR] +
                SS[Component.PART] +
                SS[Component.MEASUREMENT])
        return SS

    def calculateMS(self, dof, SS):
        """Calculate Mean of Squares."""
        MS = dict()

        for key in SS:
            MS[key] = SS[key] / dof[key]
        return MS

    def calculateGaugeVariance(self, MS):
        """Calculate GaugeRnR Variances."""
        Var = dict()

        Var[Component.MEASUREMENT] = MS[Component.MEASUREMENT]
        Var[Component.OPERATOR_BY_PART] = ((
            MS[Component.OPERATOR_BY_PART] - MS[Component.MEASUREMENT]) /
            self.parts)
        Var[Component.OPERATOR] = ((
            MS[Component.OPERATOR] - MS[Component.OPERATOR_BY_PART]) /
            (self.parts * self.measurements))
        Var[Component.PART] = ((
            MS[Component.PART] - MS[Component.OPERATOR_BY_PART]) /
            (self.operators * self.measurements))

        for key in Var:
            if Var[key] < 0:
                Var[key] = 0

        Var[Component.TOTAL] = \
            Var[Component.OPERATOR] + \
            Var[Component.PART] + \
            Var[Component.OPERATOR_BY_PART] + \
            Var[Component.MEASUREMENT]

        Var[GaugeRnR.GRR] = \
            Var[Component.MEASUREMENT] + \
            Var[Component.OPERATOR] + \
            Var[Component.OPERATOR_BY_PART]

        return Var

    def calculateGaugeStd(self, Var):
        """Calculate GaugeRnR Standard Deviations."""
        Std = dict()
        for key in Var:
            Std[key] = math.sqrt(Var[key])

        return Std

    def calculateF(self, MS):
        """Calculate F-Values."""
        F = dict()

        F[Component.OPERATOR] = (
            MS[Component.OPERATOR] /
            MS[Component.OPERATOR_BY_PART])

        F[Component.PART] = (
            MS[Component.PART] /
            MS[Component.OPERATOR_BY_PART])

        F[Component.OPERATOR_BY_PART] = (
            MS[Component.OPERATOR_BY_PART] /
            MS[Component.MEASUREMENT])

        return F

    def calculateP(self, dof, F):
        """Calculate P-Values."""
        P = dict()

        P[Component.OPERATOR] = \
            1 - stats.f.cdf(
            F[Component.OPERATOR],
            dof[Component.OPERATOR],
            dof[Component.OPERATOR_BY_PART])

        P[Component.PART] = \
            1 - stats.f.cdf(
            F[Component.PART],
            dof[Component.PART],
            dof[Component.OPERATOR_BY_PART])

        P[Component.OPERATOR_BY_PART] = \
            1 - stats.f.cdf(
            F[Component.OPERATOR_BY_PART],
            dof[Component.OPERATOR_BY_PART],
            dof[Component.MEASUREMENT])
        return P
