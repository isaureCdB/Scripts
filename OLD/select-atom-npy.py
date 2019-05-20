#!/usr/bin/env python
import numpy as np
import sys

def npy2to3(npy):
    if len(npy.shape) == 2:
        reshape = 1
        if npy.shape[1] == 3:
            npy = npy.reshape(1, npy.shape[0], npy.shape[1])
        else:
            npy = npy.reshape(npy.shape[0], int(npy.shape[1]/3), 3)
    else:
        assert len(npy.shape) == 3
        reshape = 0
    return npy, reshape

npy, reshape = npy2to3(np.load(sys.argv[1]))
outp = sys.argv[2]
sel = [ int(i)-1 for i in sys.argv[3:] ]

npy2 = npy[:, sel, :]

if reshape:
    npy2 = npy2.reshape(npy2.shape[0],npy2.shape[1]*3)

np.save(outp, npy2)
