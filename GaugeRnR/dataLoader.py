
import numpy as np


class DataLoader():

    def load(self,
             file,
             structure,
             axes,
             delimiter):
        data = np.loadtxt(fname=file, delimiter=delimiter)
        data = data.reshape(tuple(structure))
        data = np.transpose(data, axes=axes)
        return data
