#!/usr/bin/env python3

import sys
import numpy as np
from rmsdlib import multifit

def fit_multi_npy(a, ref):
    #print(np.shape(a))
    #print(np.shape(ref))
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a.sum(axis=1)/a.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return RMSD

at1 = [ int(l.split()[0])-1 for l in open(sys.argv[3]).readlines()]
at2 = [ int(l.split()[0])-1 for l in open(sys.argv[4]).readlines()]

lib1 = np.load(sys.argv[1])[:,at1]
lib2 = np.load(sys.argv[2])[:,at2]

outfile=sys.argv[5]

comp_matrix = np.zeros((len(lib1), len(lib2)))

n = 0
for conf1 in lib1:
    rmsd = fit_multi_npy(lib2, conf1)
    comp_matrix[n] = rmsd
    n+=1

np.save(outfile, comp_matrix)
