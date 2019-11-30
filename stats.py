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
        self.setupShape(data.shape)
        dof = calculateDoF(data.shape)
        SS = calculateSS(data)

        #SStot = np.sum((data-mu)**2)
        #SSO = np.sum((omu-mu)**2)
        #SSP = np.sum((pmu-mu)**2)

        #dataE = data.reshape(measurements, operators*parts)
        #SSE = np.sum((dataE-emu)**2)

        #SSOP = SStot - (SSO + SSP + SSE)

        #print("SS E: ", SSE)
        #print("SS O: ", SSO)
        #print("SS OP: ", SSOP)
        #print("SS P: ", SSP)
        #print("SS tot", SStot)

        #varTot = SStot/totDof

        #varE = SSE/eDof
        #varO = SSO/oDoF
        #varP = SSP/pDoF
        #varOP = SSOP/opDoF

        #print("Sigma tot: ", sqrt(varTot))
        #print("Sigma E: ", sqrt(varE))
        #print("Sigma O: ", sqrt(varO))
        #print("Sigma OP: ", varOP)
        #print("Sigma P: ", sqrt(varP))
        #print("Sigma tot*", sqrt(varE + varO + varP))

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
