#!/usr/bin/env python3

import sys
import numpy as np
from math import *

usage="usage: clashes-frag-in-chains.py\
 <chains> <cutoff> <spacing> <coor1.npy> <coor2.npy> [<coor3.npy> ...]"

assert len(sys.argv) > 5, usage

def npy2to3(npy):
    if len(npy.shape) == 2:
        if npy.shape[1] == 3:
            npy = npy.reshape(1, npy.shape[0], npy.shape[1])
        else:
            npy = npy.reshape(npy.shape[0], int(npy.shape[1]/3), 3)
    else:
        assert len(npy.shape) == 3
    return npy

def dist(at1, at2):
    return (sum([ (at1[i] - at2[i])**2 for i in range(3)] ))**0.5

def check(atoms1, atoms2, cutoff):
    for at1 in atoms1:
        for at2 in atoms2:
            if dist(at1, at2) < cutoff:
                return True
    return False

def get_clashes_p3(coor1, coor2, threshold):
    import cffi
    from _get_clashes_p3 import ffi
    from _get_clashes_p3.lib import get_clashes_p3
    def npdata(a):
      return a.__array_interface__["data"][0]
    n = structures.shape[0]
    nat = structures.shape[1]
    clash_matrix = np.zeros((n, n), dtype = bool)
    ptr_structures = ffi.cast("double *", npdata(structures) )
    ptr_matrix = ffi.cast("bool *", npdata(clash_matrix) )
    get_clashes_p3(n, nat, threshold, ptr_structures, ptr_matrix)
    return clash_matrix

chains = [ [int(i)-1 for i in l.split()] for l in open(sys.argv[1]).readlines()]
cutoff = float(sys.argv[2])
spacing = int(sys.argv[3])
nfrag = len(chains[0])
assert len(sys.argv) == 4 + nfrag, (len(sys.argv), 4 + nfrag)
nchains = len(chains)
coor = [ npy2to3(np.load(i)) for i in sys.argv[4: 4 + nfrag] ]

# to print not clashing chains:
for nc, chain in enumerate(chains):
    #print("%i/%i"%(nc+1, nchains), file=sys.stderr)
    clash = False
    for i in range(nfrag):
        for j in range(i + spacing, nfrag):
            atoms1, atoms2 = coor[i][chain[i]], coor[j][chain[j]]
            clash = check(atoms1, atoms2, cutoff)
            if clash:
                break
        if clash:
            break
    if not clash:
        print(nc+1)

'''
for nc, chain in enumerate(chains):
    clash = False
    for n1, i in enumerate(chain[:-3]):
        for nn2, j in enumerate(chain[n1+3:]):
            n2 = n1+nn2
            coor1, coor2 = npy[i-1], npy[j-1]
    frags = npy[chain]
    clash_matrix = get_clashes_p3(coor1, coor2, cutoff)
    for n1 in range(nfrag-3):
        for n2 in range(n1+3,nfrag):
            if clash_matrix[n1, n2]:
                print("%i : frag %i - %i "%(nc+1,n1, n2)) ###
'''
