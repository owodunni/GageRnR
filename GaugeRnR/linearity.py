import numpy as np
from tabulate import tabulate
from .statistics import Statistics, Result, Component
import statsmodels.api as sm

ResultNames = {
    Result.K: 'Linearity',
    Result.Bias: 'Bias',
    Result.P: 'P-Value'}


class Linearity(Statistics):

    title = "Linearity and Bias"

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

        headers = ['Linearity Estimate',
                   ResultNames[Result.K],
                   ResultNames[Result.Bias],
                   ResultNames[Result.P]]

        table = []
        results = [Result.K, Result.Bias, Result.P]
        self.addToTable(results, Component.TOTAL, table, precision)

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

        K[Component.TOTAL], Bias[Component.TOTAL], P[Component.TOTAL] = self.estimateCoef(means_, residuals)
        return K, Bias, P

    def estimateCoef(self, x, y):
        x = sm.add_constant(x, prepend=False)
        mod = sm.OLS(y, x)
        res = mod.fit()

        return (
            np.array([float(res.params[0])]),
            np.array([float(res.params[1])]),
            np.array([float(res.pvalues[0])]))
