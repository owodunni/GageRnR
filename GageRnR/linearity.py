import numpy as np
from tabulate import tabulate
from .statistics import Statistics, Result, Component
import statsmodels.api as sm
import plotly.graph_objects as go

ResultNames = {
    Result.K: 'Linearity',
    Result.Bias: 'Bias',
    Result.P: 'P-Value'}


class Linearity(Statistics):
    title = "Linearity and Bias"

    def __init__(self, data, partGt=None):
        super().__init__(data)
        if(partGt is None):
            self.gt = self.calculateMean()[Component.PART]
        else:
            self.gt = partGt

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
                'Linearity.calculate() should be run before calling summary()')

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

    def calculatePartResiduals(self):
        means = np.repeat(
            self.gt,
            self.measurements*self.operators)
        means = means.reshape(self.parts, self.measurements*self.operators)
        residuals = self.dataToParts() - means
        return (means.flatten(), residuals.flatten())

    def calculateLinearity(self):
        """Least square test"""
        K = dict()
        Bias = dict()
        P = dict()
        means = None

        means, residuals = self.calculatePartResiduals()

        K[Component.TOTAL], Bias[Component.TOTAL], P[Component.TOTAL] = self.estimateCoef(means, residuals)
        return K, Bias, P

    def estimateCoef(self, x, y):
        x = sm.add_constant(x, prepend=False)
        mod = sm.OLS(y, x)
        res = mod.fit()

        return (
            np.array([float(res.params[0])]),
            np.array([float(res.params[1])]),
            np.array([float(res.pvalues[0])]))

    def createLinearityPlot(self):

        X, Y = self.calculatePartResiduals()
        min = np.amin(X)
        max = np.amax(X)
        range = max - min
        x = np.linspace(0 - 10*range, max + 10*range, 2)
        y = self.result[Result.K][Component.TOTAL]*x + self.result[Result.Bias][Component.TOTAL]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=X, y=Y,
            mode='markers',
            name='residuals'))
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name='linearity'))
        fig.update_layout(
            title="Part Residual vs Part Mean",
            xaxis_title="Part Mean",
            yaxis_title="Part Residuals",
            xaxis=dict(range=[min - range/4, max + range/4])
        )
        return fig
