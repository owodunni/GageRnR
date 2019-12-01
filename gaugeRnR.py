import numpy as np
import math
import scipy.stats as stats
from enum import Enum


class Component(Enum):
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
    DF = 0
    SS = 1
    MS = 2
    Var = 3
    Std = 4
    F = 5
    P = 6


ResultNames = {
    Result.DF: 'Degrees of Freedom',
    Result.SS: 'Sum of Squares',
    Result.MS: 'Mean Square',
    Result.Var: 'Variance',
    Result.Std: 'Standard deviation',
    Result.F: 'F-value',
    Result.P: 'P-value'}


class GaugeRnR:
    GRR = 'GaugeRnR'

    def __init__(self, data):
        self.data = data
        self.parts = data.shape[1]
        self.operators = data.shape[0]
        self.measurements = data.shape[2]

    def __str__(self):
        return self.tabulateClass()

    def tabulateClass(self):
        if not hasattr(self, 'dof'):
            return 'Shape: ' + \
                str([self.operators, self.parts, self.measurements])

    def calculate(self):
        self.result = dict()
        self.result[Result.DF] = self.calculateDoF()

        self.result[Result.SS] = self.calculateSS()

        self.result[Result.MS] = self.calculateMS(
            self.result[Result.DF],
            self.result[Result.SS])

        self.result[Result.Var] = self.calculateVariance(
            self.result[Result.MS])

        self.result[Result.Std] = self.calculateStd(self.result[Result.Var])

        self.result[Result.F] = self.calculateF(self.result[Result.MS])

        self.result[Result.P] = self.calculateP(
            self.result[Result.DF],
            self.result[Result.F])

        return self.result

    def calculateDoF(self):
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

    def calculateSquares(self):
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
        squares = self.calculateSquares()
        SD = dict()
        for key in squares:
            SD[key] = np.sum(squares[key])
        return SD

    def calculateSS(self):
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
        MS = dict()

        for key in SS:
            MS[key] = SS[key] / dof[key]
        return MS

    def calculateVariance(self, MS):
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

    def calculateStd(self, Var):
        Std = dict()
        for key in Var:
            Std[key] = math.sqrt(Var[key])

        return Std

    def calculateF(self, MS):
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
