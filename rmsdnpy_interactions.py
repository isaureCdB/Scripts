#!/usr/bin/env python

import sys, os
import numpy as np
sys.path.append(os.environ["ATTRACTTOOLS"])
from rmsdlib import multifit
from npy import npy2to3, npy3to2
print >> sys.stderr, "usage: python rmsdnpy.py chains.npy Lboundr.pdb > outp"

'''
compute RMSD between pairs of connected poses in chains
TO FINISH
'''

def rmsdnpy(chains, pdb):
    chains = npy3to2(chains)
    reference = [ l for l in open(pdb).readlines() if l.startswith("ATOM") ]
    r = [ [float(l[30:38]), float(l[38:46]), float(l[46:54])] for l in reference]
    ref = np.array(r)
    print >> sys.stderr, chains.shape
    ref = ref.reshape(ref.shape[0]*ref.shape[1])
    ncoord = np.shape(chains[0])[0]
    print >> sys.stderr,  (np.shape(chains), np.shape(ref))
    RMSD = [ (sum([(chain[i]-ref[i])**2 for i in range(ncoord)]) /(ncoord/3))**0.5 for chain in chains ]
    return RMSD

def pairwise_rmsdnpy(a, b):
    a = npy3to2(a)
    b = npy3to2(b)
    ncoord = np.shape(a[0])[0]
    print >> sys.stderr,  (np.shape(a), np.shape(b))
    RMSD = np.array([[(sum([(a1[i]-b1[i])**2 for i in range(ncoord)]) /(ncoord/3))**0.5  for b1 in b] for a1 in a])
    return RMSD

chainsfile = sys.argv[1]    # chains.npy
interactionsfile = sys.argv[2] # interactions.npy

chains = np.load(chainsfile)
interactions = np.load(interactionsfile)

print >> sys.stderr,  np.shape(chains)
poses1 = interactions[:,0]

for p1 in poses1:
    p2 = [ i[1] for i in interaction if i[0]==p1]

RMSD = rmsdnpy(chains, pdb)
for i in range(len(RMSD)):
    print i+1, str(0.01*round(100*(RMSD[i])))
