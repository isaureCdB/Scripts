#!/usr/bin/env python3

import sys
import numpy as np
from math import *

usage="usage: clashes-frag-in-chains.py\
 <chains> <nfrag> <spacing> <nat> <coor1.npy> <coor2.npy> [<coor3.npy> ...]"

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

def mindist(atoms1, atoms2):
    m = 1000
    dif = atoms1[:, None] - atoms2[None, :]
    dist = np.sum(dif*dif, axis=2).min()
    dist = dist**0.5
    return dist

nfrag = int(sys.argv[2])
chains = [ [int(i)-1 for i in l.split()[3:3+nfrag]] for l in open(sys.argv[1]).readlines()[1:]]
spacing = int(sys.argv[3])
nat = [int(i) for i in sys.argv[4].split(" ")] # "6 6 6" for UUU
assert len(nat) == 3 , "nat = at per nucl in homotrimer"
assert len(sys.argv) == 5 + nfrag, (len(sys.argv), 5 + nfrag)
nchains = len(chains)
coor = [ npy2to3(np.load(i)) for i in sys.argv[5: 5 + nfrag] ]

# to print not clashing chains:

for nc, chain in enumerate(chains):
    if not nc%10000: print("%i/%i"%(nc, nchains), file=sys.stderr)
    m = []
    for i in range(nfrag):
        for j in range(i + spacing, nfrag):
            aa1 = 0
            for n1 in range(3):
                aa2 = 0
                for n2 in range(3):
                    a1, a2 = nat[n1], nat[n2]
                    atoms1 = coor[i][chain[i]][aa1: aa1+a1]
                    atoms2 = coor[j][chain[j]][aa2: aa2+a2]
                    aa2 += a2
                    m.append(mindist(atoms1, atoms2))
                aa1 += a1
    m.sort()
    print(nc+1, end=" "),
    for mm in m[:-1]:
        print("%.1f"%mm, end=" ")
    print("%.1f"%m[-1])

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
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/mindist-frag-in-chains-pernucl.py
