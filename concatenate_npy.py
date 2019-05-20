#!/usr/bin/env python3

import numpy as np
import sys, argparse

def npy2to3(npy):
    if len(npy.shape) == 2:
        if npy.shape[1] == 3:
            npy = npy.reshape(1, npy.shape[0], npy.shape[1])
        else:
            npy = npy.reshape(npy.shape[0], int(npy.shape[1]/3), 3)
    else:
        assert len(npy.shape) == 3
    return npy

def npy3to2(npy):
    if len(npy.shape) == 3:
        npy = npy.reshape(npy.shape[0], 3*npy.shape[1])
    else:
        assert len(npy.shape) == 2 and npy.shape[1]%3 == 0
    return npy

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('npy1', help="np array")
parser.add_argument('npy2', help="np array")
parser.add_argument('--one2all', help="distribute npy1 to all in npy2", action="store_true")
parser.add_argument('--outp', help="outut npy file")

args = parser.parse_args()
############

a = npy2to3(np.load(args.npy1))
b = npy2to3(np.load(args.npy2))


if args.one2all:
    n = b.shape[0]
    a = np.array([a[0] for i in range(n) ])
    print(a.shape)
else:
    assert len(a.shape)== len(b.shape), (a.shape, b.shape)
    assert a.shape[1]== b.shape[1], (a.shape, b.shape)
    assert a.shape[2]== 3 and b.shape[2]==3, (a.shape, b.shape)

print((a.shape, b.shape))

c=np.concatenate((a,b), axis=1)

print(c.shape)

np.save(args.outp, c)
