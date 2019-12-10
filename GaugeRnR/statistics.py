

class Statistics(object):
    def __init__(self, data):
        self.data = data
        self.parts = data.shape[1]
        self.operators = data.shape[0]
        self.measurements = data.shape[2]