#!/usr/bin/env python3

import sys
import numpy as np
from math import *

coor = np.load(sys.argv[1])
if coor.ndim == 2:
    coor = coor.reshape((1, coor.shape[0], coor.shape[1]))
assert coor.ndim == 3
at1 = int(sys.argv[2])-1
at2 = int(sys.argv[3])-1

atoms1 = coor[:, at1, :]
atoms0 = coor[:, at2, :]

d = (atoms1-atoms0)**2
d = np.sqrt(d.sum(axis=1))
for i in d:
    print(i)
