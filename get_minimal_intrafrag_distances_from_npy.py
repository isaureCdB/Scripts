#!/usr/bin/env python3
from math import *
import sys
import numpy as np

def get_min_dist(coor, sel1, sel2):
    if coor.ndim == 2:
        coor = coor.reshape((1, coor.shape[0], coor.shape[1]))
    assert coor.ndim == 3
    csel1 = coor[:, sel1, None, :]
    csel2 = coor[:, None, sel2, :]
    d = np.sum((csel2 - csel1)**2, axis=3)
    d = d.reshape((len(coor), len(sel1)*len(sel2)))
    mind = (np.min(d, axis=1))**0.5
    return mind

npy = sys.argv[1]           # TGG-fit-sel0.2.npy
template = sys.argv[2]      # ~/projets/ssDNA/dnalib/trilib/TGG/conf-aa-1.pdb
clean_frag = sys.argv[3]    # clean_fragments (list of fragments without missing atoms
                            #   = output from ~/Scripts/get_clean_fragments.py)
seq = sys.argv[4]           # TGG

# To check only a selectio nof structures (e.g. cluster centers)
sel = None
if len(sys.argv) > 5:
    sel = sys.argv[5]

outp = open(seq+'.mindist-clean','w')

# atom modified by A-C => G-U/T mutations
mut_atoms = { "A" : ["N2", "O2", "O6"],
              "G" : ["N2", "O2", "O6"],
              "T" : ["N4", "O4", "C7"],
              "C" : ["N4", "O4", "C7"],
              "U" : ["N4", "O4", "C7"],
              }

ll = [l for l in open(template).readlines() if l.startswith("ATOM")]

# get indices of atoms in each residue
prev = None
at_indices = [[]]
count = 0
for l in ll:
    resid = int(l[22:26])
    if resid != prev and prev != None:
        at_indices.append([])
    at_indices[-1].append(count)
    prev = resid
    count += 1

'''
ATOM      2  O1P  DG     1       3.643   5.134   7.857   92  -0.660 0 1.00
'''

elements = set([l[13] for l in ll])

indices1, indices2 = {}, {}
for n in elements:
    indices1[n] = []
    indices2[n] = []

for nl, l in enumerate(ll):
    base = l[19]
    n = l[13]
    if l[13:15] not in mut_atoms[base]:
        if nl in at_indices[0]:
            indices1[n].append(nl)
        if nl in at_indices[1]:
            indices2[n].append(nl)

# select fragment that had no missing atoms in the original PDB
# (don't check atoms created by mutation)
lll = open(clean_frag).readlines()
ll = [l.split() for l in open(clean_frag).readlines()]
ind_clean = [ int(l[1])-1 for l in ll if l[0] == seq ]
coor = np.load(npy)
if coor.ndim == 2:
    coor = coor.reshape((1, len(coor)))

#print(coor.shape)
if sel is None:
    coor = np.load(npy)[ind_clean]
else:
    centers = [ int(l)-1 for l in open(sel).readlines() ]
    ind_clean = [ni for ni, i in enumerate(centers) if i in ind_clean]
    coor = np.load(npy)[ind_clean]

written = set()
for n1 in elements:
    for n2 in elements:
        min_dist1 = get_min_dist(coor, indices1[n1], indices2[n2])
        mintot = min_dist1
        if n1 != n2:
            min_dist2 = get_min_dist(coor, indices1[n2], indices2[n1])
            mintot = [ min(a,b) for a, b in zip(min_dist1, min_dist2) ]
        if n1+n2 not in written:
            for ni, i in enumerate(mintot):
                print("%s %s %i %0.2f"%(n1, n2, ind_clean[ni]+1, i), file=outp)
            written.add(n1+n2)
            written.add(n2+n1)

outp.close()
