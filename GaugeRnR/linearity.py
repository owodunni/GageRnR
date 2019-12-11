import numpy as np
from tabulate import tabulate
from .statistics import Statistics, Result, Component

ResultNames = {
    Result.K: 'Linearity',
    Result.Bias: 'Bias',
    Result.P: 'P-Value'}


class Linearity(Statistics):
    def __init__(self, data):
        super().__init__(data)

    def calculate(self):
        """Calculate Linearity."""
        self.result = dict()
        self.result[Result.K], self.result[Result.Bias], self.result[Result.P] = \
            self.calculateLinearity()

        return self.result

    def summary(self, tableFormat="fancy_grid", precision='.3f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'Linearity.calcualte() should be run before calling summary()')

        headers = ['Sources of Normality',
                   ResultNames[Result.K],
                   ResultNames[Result.Bias],
                   ResultNames[Result.P]]

        table = []

        return tabulate(
            table,
            headers=headers,
            tablefmt=tableFormat)

    def calculateLinearity(self, partGt=None):
        """Least square test"""
        K = dict()
        Bias = dict()
        P = dict()
        means = None

        if(partGt is None):
            means = self.calculateMean()[Component.PART]
        else:
            means = partGt

        means_ = np.repeat(
            means,
            self.measurements*self.operators)
        means_ = means_.reshape(self.parts, self.measurements*self.operators)
        residuals = self.dataToParts() - means_

        means_ = means_.flatten()
        residuals = residuals.flatten()

        print("Hello")
        K[Component.TOTAL], Bias[Component.TOTAL] = self.estimateCoef(means_, residuals)
        return K, Bias, P

    def estimateCoef(self, x, y):
        # number of observations/points
        n = np.size(x)

        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)

        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x

        # calculating regression coefficients
        K = SS_xy / SS_xx
        bias = m_y - K*m_x

        return(K, bias)
