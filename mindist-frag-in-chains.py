#!/usr/bin/env python3

import sys
import numpy as np
from math import *

usage="usage: <chains> <nfrag> <spacing> <coor1.npy> <coor2.npy> [<coor3.npy> ...]"

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

#chainlines = [l for l in open(sys.argv[1]).readlines()[1:]]
chainlines = [l for l in open(sys.argv[1]).readlines() if not l.startswith("#")]
nfrag = int(sys.argv[2])
spacing = int(sys.argv[3])
coor = [ npy2to3(np.load(i)) for i in sys.argv[4: 4 + nfrag] ]

assert len(sys.argv) == 4 + nfrag, (len(sys.argv), 4 + nfrag)
#chains = [ [int(i)-1 for i in l.split()[2:2+nfrag]] for l in chainlines]
c = chainlines[0].split()
for i in range(len(c)):
    try:
        int(c[i])
        break
    except:
        continue
print(i, file=sys.stderr)
chains = np.array([ [int(i)-1 for i in l.split()[i:i+nfrag]] for l in chainlines] )

nchains = len(chains)

print("#", end=" ")
for i in range(nfrag):
    for j in range(i + spacing, nfrag):
        print("%i-%i "%(i+1, j+1), end=" ")
print("")

# to print not clashing chains:
for nc, chain in enumerate(chains):
    if not nc%10000: print("%i/%i"%(nc, nchains), file=sys.stderr)
    m = []
    print(nc+1, end=" "),
    for i in range(nfrag):
        for j in range(i + spacing, nfrag):
            atoms1 = coor[i][chain[i]]
            try:
                atoms2 = coor[j][chain[j]]
            except:
                #print((j, len(chain)), file=sys.stderr)
                sys.exit()
            mm = mindist(atoms1, atoms2)
            print(" %.1f"%mm, end="")
    print(" ")

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
