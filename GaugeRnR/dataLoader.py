
import numpy as np


class DataLoader():

    def load(self,
             file,
             structure,
             axes,
             delimiter):
        data = np.loadtxt(fname=file, delimiter=delimiter)
        s = (structure[axes[0]],
            structure[axes[1]],
            structure[axes[2]])
        data = data.reshape(s)
        data = np.transpose(data, axes=axes)
        data = data.reshape(tuple(structure))
        return data
