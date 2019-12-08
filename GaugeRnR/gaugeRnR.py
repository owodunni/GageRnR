"""Module containing the algorithm for GaugeRnR."""
import numpy as np
import math
import scipy.stats as stats
from tabulate import tabulate
from .statistics import Statistics as st


class GaugeRnR(st):
    """Main class for calculating GaugeRnR."""

    GRR = 'GaugeRnR'

    def __init__(self, data):
        st.__init__(self, data)

    def __str__(self):
        """Enum containing the measurements calculated by GaugeRnR."""
        if not hasattr(self, 'result'):
            return 'Shape: ' + \
                str([self.operators, self.parts, self.measurements])
        return self.summary()

    def summary(self, tableFormat="fancy_grid", precision='.3f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'GaugeRnR.calcualte() should be run before calling summary()')

        headers = ['Sources of Variance']

        for key in st.ResultNames:
            headers.append(st.ResultNames[key])

        table = []
        for comp in st.Component:
            innerTable = [st.ComponentNames[comp]]
            for key in st.ResultNames:
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
        self.result[st.Result.DF] = self.calculateDoF()
        self.result[st.Result.Mean] = self.calculateMean()
        self.result[st.Result.SS] = self.calculateSS()

        self.result[st.Result.MS] = self.calculateMS(
            self.result[st.Result.DF],
            self.result[st.Result.SS])

        self.result[st.Result.Var] = self.calculateVar(
            self.result[st.Result.MS])

        self.result[st.Result.Std] = self.calculateStd(self.result[st.Result.Var])

        self.result[st.Result.F] = self.calculateF(self.result[st.Result.MS])

        self.result[st.Result.P] = self.calculateP(
            self.result[st.Result.DF],
            self.result[st.Result.F])

        return self.result

    def calculateDoF(self):
        """Calculate Degrees of freedom."""
        oDoF = self.operators - 1
        pDoF = self.parts - 1
        opDoF = (self.parts - 1) * (self.operators - 1)
        eDof = self.parts * self.operators * (self.measurements - 1)
        totDof = self.parts * self.operators * self.measurements - 1
        return {
            st.Component.OPERATOR: oDoF,
            st.Component.PART: pDoF,
            st.Component.OPERATOR_BY_PART: opDoF,
            st.Component.MEASUREMENT: eDof,
            st.Component.TOTAL: totDof}

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
            st.Component.TOTAL: mu,
            st.Component.OPERATOR: omu,
            st.Component.PART: pmu,
            st.Component.MEASUREMENT: emu}

    def calculateSquares(self):
        """Calculate Squares."""
        mean = self.calculateMean()
        tS = (self.data - mean[st.Componen.TOTAL])**2
        oS = (mean[st.Componen.OPERATOR] - mean[st.Componen.TOTAL])**2
        pS = (mean[st.Componen.PART] - mean[st.Componen.TOTAL])**2

        dataE = self.data.reshape(
            self.operators * self.parts,
            self.measurements)
        meanMeas = np.repeat(mean[st.Componen.MEASUREMENT], self.measurements)
        meanMeas = meanMeas.reshape(
            self.operators * self.parts,
            self.measurements)

        mS = (dataE - meanMeas)**2
        return {
            st.Componen.TOTAL: tS,
            st.Componen.OPERATOR: oS,
            st.Componen.PART: pS,
            st.Componen.MEASUREMENT: mS}

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

        SS[st.Componen.OPERATOR] = \
            self.parts * self.measurements * \
            SS[st.Componen.OPERATOR]
        SS[st.Componen.PART] = \
            self.operators * self.measurements * \
            SS[st.Componen.PART]
        SS[st.Componen.OPERATOR_BY_PART] = \
            SS[st.Componen.TOTAL] - (
                SS[st.Componen.OPERATOR] +
                SS[st.Componen.PART] +
                SS[st.Componen.MEASUREMENT])
        return SS

    def calculateMS(self, dof, SS):
        """Calculate Mean of Squares."""
        MS = dict()

        for key in SS:
            MS[key] = SS[key] / dof[key]
        return MS

    def calculateVar(self, MS):
        """Calculate GaugeRnR Variances."""
        Var = dict()

        Var[st.Componen.MEASUREMENT] = MS[st.Componen.MEASUREMENT]
        Var[st.Componen.OPERATOR_BY_PART] = ((
            MS[st.Componen.OPERATOR_BY_PART] - MS[st.Componen.MEASUREMENT]) /
            self.parts)
        Var[st.Componen.OPERATOR] = ((
            MS[st.Componen.OPERATOR] - MS[st.Componen.OPERATOR_BY_PART]) /
            (self.parts * self.measurements))
        Var[st.Componen.PART] = ((
            MS[st.Componen.PART] - MS[st.Componen.OPERATOR_BY_PART]) /
            (self.operators * self.measurements))

        for key in Var:
            if Var[key] < 0:
                Var[key] = 0

        Var[st.Componen.TOTAL] = \
            Var[st.Componen.OPERATOR] + \
            Var[st.Componen.PART] + \
            Var[st.Componen.OPERATOR_BY_PART] + \
            Var[st.Componen.MEASUREMENT]

        Var[GaugeRnR.GRR] = \
            Var[st.Componen.MEASUREMENT] + \
            Var[st.Componen.OPERATOR] + \
            Var[st.Componen.OPERATOR_BY_PART]

        return Var

    def calculateStd(self, Var):
        """Calculate GaugeRnR Standard Deviations."""
        Std = dict()
        for key in Var:
            Std[key] = math.sqrt(Var[key])

        return Std

    def calculateF(self, MS):
        """Calculate F-Values."""
        F = dict()

        F[st.Componen.OPERATOR] = (
            MS[st.Componen.OPERATOR] /
            MS[st.Componen.OPERATOR_BY_PART])

        F[st.Componen.PART] = (
            MS[st.Componen.PART] /
            MS[st.Componen.OPERATOR_BY_PART])

        F[st.Componen.OPERATOR_BY_PART] = (
            MS[st.Componen.OPERATOR_BY_PART] /
            MS[st.Componen.MEASUREMENT])

        return F

    def calculateP(self, dof, F):
        """Calculate P-Values."""
        P = dict()

        P[st.Componen.OPERATOR] = \
            stats.f.sf(
            F[st.Componen.OPERATOR],
            dof[st.Componen.OPERATOR],
            dof[st.Componen.OPERATOR_BY_PART])

        P[st.Componen.PART] = \
            stats.f.sf(
            F[st.Componen.PART],
            dof[st.Componen.PART],
            dof[st.Componen.OPERATOR_BY_PART])

        P[st.Componen.OPERATOR_BY_PART] = \
            stats.f.sf(
            F[st.Componen.OPERATOR_BY_PART],
            dof[st.Componen.OPERATOR_BY_PART],
            dof[st.Componen.MEASUREMENT])
        return P
