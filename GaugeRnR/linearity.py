import numpy as np
from scipy.stats import shapiro
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

    def calculateLinearity(self):
        """Shapiro-Wilk Test"""
        K = dict()
        Bias = dict()
        P = dict()
        return K, Bias, P
