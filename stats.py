import numpy as np
from math import sqrt

class GaugeRnR:
    OPERATOR='operator'
    PART='part'
    MEASUREMENT='measurment'
    OPERATOR_BY_PART='operator by part'
    TOTAL='total'

    def __init__(self, shape):
        self.parts = shape[1]
        self.operators = shape[0]
        self.measurements = shape[2]

    def calculate(self, data):
        self.dof = self.calculateDoF()
        self.SS = self.calculateSS(data)
        
        self.MS = dict()

        for key in self.SS:
            self.MS[key] = self.SS[key]/self.dof[key]

    def calculateDoF(self):
        oDoF = self.operators - 1
        pDoF = self.parts - 1
        opDoF = (self.parts - 1)*(self.operators - 1)
        eDof = self.parts*self.operators*(self.measurements - 1)
        totDof = self.parts*self.operators*self.measurements - 1
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
        emu = emu.reshape(self.parts*self.operators)

        return {
            GaugeRnR.TOTAL : mu,
            GaugeRnR.OPERATOR: omu,
            GaugeRnR.PART: pmu,
            GaugeRnR.MEASUREMENT: emu}
    
    def calculateSquares(self, data):
        mean = self.calculateMean(data)
        tS = (data-mean[GaugeRnR.TOTAL])**2
        oS = (mean[GaugeRnR.OPERATOR]-mean[GaugeRnR.TOTAL])**2
        pS = (mean[GaugeRnR.PART]-mean[GaugeRnR.TOTAL])**2

        dataE = data.reshape(self.operators*self.parts, self.measurements)
        meanMeas = np.repeat(mean[GaugeRnR.MEASUREMENT],self.measurements)
        meanMeas = meanMeas.reshape(self.operators*self.parts, self.measurements)

        mS = (dataE-meanMeas)**2
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
                SS[GaugeRnR.OPERATOR] + \
                SS[GaugeRnR.PART] + \
                SS[GaugeRnR.MEASUREMENT])
        return SS
