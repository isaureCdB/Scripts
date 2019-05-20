#!/usr/bin/env python3

import sys
import numpy as np
from math import *

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

structures = npy2to3(np.load(sys.argv[1])) #chain2rna.npy
cutoff = float(sys.argv[2])
spacing = int(sys.argv[3]) # clashes res(i)-res(i+spacing)
sel = [int(l.split()[0])-1 for l in open(sys.argv[4]).readlines()]
structures = structures[sel]
natoms = [int(i) for i in sys.argv[5:]]
#print natoms
assert sum(natoms) == structures.shape[1]
nres = len(natoms)
nstruc = structures.shape[0]

count = 0
residues = []
for i in natoms:
    residues.append(structures[:,list(range(count,count + i))])
    count += i

clashes = open(sys.argv[1].split(".npy")[0] + ".clashes-%iA-spacing%i"%(cutoff, spacing), "w")
for i in range(nstruc):
    clash = False
    for res1 in range(nres):
        for res2 in range(res1+spacing, nres):
            atoms1, atoms2 = residues[res1][i], residues[res2][i]
            clash = check(atoms1, atoms2, cutoff)
            if clash:
                break
        if clash:
            break
    if not clash:
        print(sel[i]+1)
