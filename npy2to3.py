#!/usr/bin/env python3

import sys, os
import numpy as np
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from rmsdlib import multifit

def npy2to3(npy):
    if len(npy.shape) == 2:
        if npy.shape[1] == 3:
            npy = npy.reshape(1, npy.shape[0], npy.shape[1])
        else:
            npy = npy.reshape(npy.shape[0], int(npy.shape[1]/3), 3)
    else:
        assert len(npy.shape) == 3
    return npy

inp = np.load(sys.argv[1])
outp = sys.argv[2]

npy = npy2to3(inp)
np.save(outp, npy)
