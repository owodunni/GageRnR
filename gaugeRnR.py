import numpy as np
import math
import scipy.stats as stats


class GaugeRnR:
    OPERATOR = 'operator'
    PART = 'part'
    MEASUREMENT = 'measurment'
    OPERATOR_BY_PART = 'operator by part'
    TOTAL = 'total'
    GRR = 'GaugeRnR'

    def __init__(self, shape):
        self.parts = shape[1]
        self.operators = shape[0]
        self.measurements = shape[2]

    def __str__(self):
        return "GaugeRnR:" + "\n" +\
            GaugeRnR.OPERATOR + "s " + str(self.operators) + \
            ", " + GaugeRnR.PART + "s " + str(self.parts) + \
            ", " + GaugeRnR.MEASUREMENT + "s " + str(self.measurements)

    def calculate(self, data):
        self.dof = self.calculateDoF()
        self.SS = self.calculateSS(data)
        self.MS = self.calculateMS(self.dof, self.SS)
        self.Var = self.calculateVariance(self.MS)
        self.Std = self.calculateStd(self.Var)
        self.F = self.calculateF(self.MS)
        self.P = self.calculateP(self.dof, self.F)

    def calculateDoF(self):
        oDoF = self.operators - 1
        pDoF = self.parts - 1
        opDoF = (self.parts - 1) * (self.operators - 1)
        eDof = self.parts * self.operators * (self.measurements - 1)
        totDof = self.parts * self.operators * self.measurements - 1
        return {
            GaugeRnR.OPERATOR: oDoF,
            GaugeRnR.PART: pDoF,
            GaugeRnR.OPERATOR_BY_PART: opDoF,
            GaugeRnR.MEASUREMENT: eDof,
            GaugeRnR.TOTAL: totDof}

    def calculateMean(self, data):
        mu = np.mean(data)

        omu = np.mean(data, axis=1)
        omu = np.mean(omu, axis=1)

        pmu = np.mean(data, axis=0)
        pmu = np.mean(pmu, axis=1)

        emu = np.mean(data, axis=2)
        emu = emu.reshape(self.parts * self.operators)

        return {
            GaugeRnR.TOTAL: mu,
            GaugeRnR.OPERATOR: omu,
            GaugeRnR.PART: pmu,
            GaugeRnR.MEASUREMENT: emu}

    def calculateSquares(self, data):
        mean = self.calculateMean(data)
        tS = (data - mean[GaugeRnR.TOTAL])**2
        oS = (mean[GaugeRnR.OPERATOR] - mean[GaugeRnR.TOTAL])**2
        pS = (mean[GaugeRnR.PART] - mean[GaugeRnR.TOTAL])**2

        dataE = data.reshape(self.operators * self.parts, self.measurements)
        meanMeas = np.repeat(mean[GaugeRnR.MEASUREMENT], self.measurements)
        meanMeas = meanMeas.reshape(
            self.operators * self.parts,
            self.measurements)

        mS = (dataE - meanMeas)**2
        return {
            GaugeRnR.TOTAL: tS,
            GaugeRnR.OPERATOR: oS,
            GaugeRnR.PART: pS,
            GaugeRnR.MEASUREMENT: mS}

    def calculateSumOfDeviations(self, data):
        squares = self.calculateSquares(data)
        SD = dict()
        for key in squares:
            SD[key] = np.sum(squares[key])
        return SD

    def calculateSS(self, data):
        SS = self.calculateSumOfDeviations(data)

        SS[GaugeRnR.OPERATOR] = \
            self.parts * self.measurements * \
            SS[GaugeRnR.OPERATOR]
        SS[GaugeRnR.PART] = \
            self.operators * self.measurements * \
            SS[GaugeRnR.PART]
        SS[GaugeRnR.OPERATOR_BY_PART] = \
            SS[GaugeRnR.TOTAL] - (
                SS[GaugeRnR.OPERATOR] +
                SS[GaugeRnR.PART] +
                SS[GaugeRnR.MEASUREMENT])
        return SS

    def calculateMS(self, dof, SS):
        MS = dict()

        for key in SS:
            MS[key] = SS[key] / dof[key]
        return MS

    def calculateVariance(self, MS):
        Var = dict()

        Var[GaugeRnR.MEASUREMENT] = MS[GaugeRnR.MEASUREMENT]
        Var[GaugeRnR.OPERATOR_BY_PART] = ((
            MS[GaugeRnR.OPERATOR_BY_PART] - MS[GaugeRnR.MEASUREMENT]) /
            self.parts)
        Var[GaugeRnR.OPERATOR] = ((
            MS[GaugeRnR.OPERATOR] - MS[GaugeRnR.OPERATOR_BY_PART]) /
            (self.parts * self.measurements))
        Var[GaugeRnR.PART] = ((
            MS[GaugeRnR.PART] - MS[GaugeRnR.OPERATOR_BY_PART]) /
            (self.operators * self.measurements))

        for key in Var:
            if Var[key] < 0:
                Var[key] = 0

        Var[GaugeRnR.TOTAL] = \
            Var[GaugeRnR.OPERATOR] + \
            Var[GaugeRnR.PART] + \
            Var[GaugeRnR.OPERATOR_BY_PART] + \
            Var[GaugeRnR.MEASUREMENT]

        Var[GaugeRnR.GRR] = \
            Var[GaugeRnR.MEASUREMENT] + \
            Var[GaugeRnR.OPERATOR] + \
            Var[GaugeRnR.OPERATOR_BY_PART]

        return Var

    def calculateStd(self, Var):
        Std = dict()
        for key in Var:
            Std[key] = math.sqrt(Var[key])

        return Std

    def calculateF(self, MS):
        F = dict()

        F[GaugeRnR.OPERATOR] = (
            MS[GaugeRnR.OPERATOR] /
            MS[GaugeRnR.OPERATOR_BY_PART])

        F[GaugeRnR.PART] = (
            MS[GaugeRnR.PART] /
            MS[GaugeRnR.OPERATOR_BY_PART])

        F[GaugeRnR.OPERATOR_BY_PART] = (
            MS[GaugeRnR.OPERATOR_BY_PART] /
            MS[GaugeRnR.MEASUREMENT])

        return F

    def calculateP(self, dof, F):
        P = dict()

        P[GaugeRnR.OPERATOR] = \
            1 - stats.f.cdf(
            F[GaugeRnR.OPERATOR],
            dof[GaugeRnR.OPERATOR],
            dof[GaugeRnR.OPERATOR_BY_PART])

        P[GaugeRnR.PART] = \
            1 - stats.f.cdf(
            F[GaugeRnR.PART],
            dof[GaugeRnR.PART],
            dof[GaugeRnR.OPERATOR_BY_PART])

        P[GaugeRnR.OPERATOR_BY_PART] = \
            1 - stats.f.cdf(
            F[GaugeRnR.OPERATOR_BY_PART],
            dof[GaugeRnR.OPERATOR_BY_PART],
            dof[GaugeRnR.MEASUREMENT])
        return P
