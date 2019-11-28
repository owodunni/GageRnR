import numpy as np

# y_ijk = u + pi + oj +(PO)ij+eijk 
# measurments: [o1:[p1:[m1, m2, m3],p2:[m1,m2,m3]],
#               o2:[p1:[m1, m2, m3],p2:[m1,m2,m3]]


class Distribution:
    def _init_(self, number, mean, sigma):
        if(number)
        self.number = number
        self.mean = mean
        self.sigma = sigma

class Settings:
    def _init_(self, operators, parts, measurments):
        self.operators = operators
        self.parts = parts
        self.measurments = measurments
        self.size = [operators.number, parts.number, measurments.number]

class Generator:
    def _init_(self, settings):
        self.settings = settings
        self.data = np.empty(settings.size)