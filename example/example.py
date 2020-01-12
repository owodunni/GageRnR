#!/usr/bin/env python3
"""Example showing how to use GageRnR."""
from GageRnR import GageRnR
import numpy as np

data = np.array(
    [[[3.29, 3.41, 3.64],
      [2.44, 2.32, 2.42],
      [4.34, 4.17, 4.27],
      [3.47, 3.5, 3.64],
      [2.2, 2.08, 2.16]],
     [[3.08, 3.25, 3.07],
      [2.53, 1.78, 2.32],
      [4.19, 3.94, 4.34],
      [3.01, 4.03, 3.2],
      [2.44, 1.8, 1.72]],
     [[3.04, 2.89, 2.85],
      [1.62, 1.87, 2.04],
      [3.88, 4.09, 3.67],
      [3.14, 3.2, 3.11],
      [1.54, 1.93, 1.55]]])

g = GageRnR(data)
g.calculate()
print(g.summary())
