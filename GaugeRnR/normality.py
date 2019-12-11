import numpy as np
from scipy.stats import shapiro
from tabulate import tabulate
from .statistics import Statistics, Result, Component, ComponentNames

#ResultNames = {
#    Result.DF: 'DF',
#    Result.SS: 'SS',
#    Result.MS: 'MS',
#    Result.Var: 'Var (\u03C3\u00B2)',
#    Result.Std: 'Std (\u03C3)',
#    Result.F: 'F-value',
#    Result.P: 'P-value'}


class Normality(Statistics):
    def __init__(self, data):
        super().__init__(data)
    
    def calculate(self):
        """Calculate GaugeRnR."""
        self.result = dict()
        self.result[Result.W], self.result[Result.W] = \
            calculateNormality()

        return self.result

    def calculateNormality(self):
        """Shapiro-Wilk Test"""
        W = dict()
        P = dict()
        W[Component.TOTAL], P[Component.TOTAL] = \
            self.shapiro()
        
        W[Component.OPERATOR], P[Component.OPERATOR] = \
            self.shapiro(axis=0)
        
        W[Component.PART], P[Component.PART] = \
            self.shapiro(axis=1)
        
        return W, P
    
    def shapiro(self, axis=-1):
        if(axis < 0):
            W, P = shapiro(self.data)
            return np.array(W), np.array(P)

        if(axis > len(self.data.shape)):
            raise AttributeError("Axis larger then dimensionality of data.")
        
        size = self.data.shape[axis]
        W = np.zeros((size))
        P = np.zeros((size))


        for i in range(0,size):
            if(axis == 0):
                W[i], P[i] = shapiro(self.data[i,:,:])
            elif(axis == 1):
                W[i], P[i] = shapiro(self.data[:,i,:])

        return W, P

