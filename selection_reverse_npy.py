#!/usr/bin/env python3
import numpy as np, sys
from npy import npy3to2

a = npy3to2(np.load(sys.argv[1]))
b = npy3to2(np.load(sys.argv[2]))

assert a.shape[1:] == b.shape[1:], "difference in arrays' shapes"
print((a.shape, b.shape), file=sys.stderr)
for i in range(b.shape[0]):
    print(1 + np.where(np.all(a==b[i],axis=1))[0][0])
