#!/usr/bin/env python3

import sys
import numpy as np
from scipy.spatial.distance import cdist
from npy import npy2to3

''' usage="usage: <rna.npy> <bound_rna.pdb> <min_spacing> '''

rna = npy2to3(np.load(sys.argv[1])) #rna.npy
bound = sys.argv[2] # bound_rna.pdb
s = int(sys.argv[3]) #min_spacing = 3
outp = sys.argv[4]

newres =  []
resnum = ""
i = 0
for l in open(bound, "r").readlines():
    if not l.startswith("ATOM"): continue
    if l[22:26] != resnum:
        newres.append(i)
    i+=1
    resnum = l[22:26]
newres.append(i)

print(newres)
nat = len(newres)

ndist = 0
print("#", end=" ")
for i in range(nat - s):
    for j in range(i + s, nat-1):
        print("%i-%i "%(i+1, j+1), end=" ")
        ndist += 1
print("")

min_dist = np.zeros((rna.shape[0], ndist))

nat = len(newres)
n = 0
for i in range(nat - s):
    res1 = rna[:, newres[i]:newres[i+1]]
    for j in range(i+s, nat-1):
        print("%i %i"%(i,j), file=sys.stderr)
        res2 = rna[:, newres[j]:newres[j+1]]
        diff = (res1[:,:,None,:] - res2[:,None,:,:])**2
        dist = (diff.sum(axis=3))**0.5
        d = dist.reshape(-1,36)
        min_dist[:, n] = d.min(axis=1)
        n += 1

np.save(outp, min_dist)
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/mindist-nucl-in-rna.py
