#!/usr/bin/env python

import numpy as np
import sys, argparse, os
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
sys.path.insert(0, os.environ["SCRIPTS"])
from rmsdlib import multifit

def npy2to3(npy):
    if len(npy.shape) == 2:
        npy = npy.reshape(npy.shape[0], npy.shape[1]/3, 3)  
    else:
        assert len(npy.shape) == 3
    return npy
    
def npy3to2(npy):
    if len(npy.shape) == 3:
        npy = npy.reshape(npy.shape[0], 3*npy.shape[1])  
    else:
        assert len(npy.shape) == 2 and npy.shape[1]%3 == 0
    return npy

def fit_multi_npy(a, ref):
    a = npy2to3(a)
    COM = a.sum(axis=1)/a.shape[1]
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None, :]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

def rmsdnpy(chains, pdb):
    chains = npy3to2(chains)
    reference = [ l for l in open(pdb).readlines() if l.startswith("ATOM") ]
    r = [ [float(l[30:38]), float(l[38:46]), float(l[46:54])] for l in reference]
    ref = np.array(r)
    ref = ref.reshape(ref.shape[0]*ref.shape[1])
    ncoord = np.shape(chasins[0])[0]
    RMSD = [ (sum([(chain[i]-ref[i])**2 for i in range(ncoord)]) /(ncoord/3))**0.5 for chain in chains ]
    return RMSD

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('cg_npy')
parser.add_argument('aa_npy')
parser.add_argument('--lib', nargs='+', help="list of monomer libraries")
parser.add_argument('--noext', help="do not replace termini", action="store_true")
args = parser.parse_args()
############
chains = np.load(args.cg_npy)
libraries = [ np.load(lib) for lib in args.lib ]
#libraries = [ np.load("../../monomers_library/"+lib+"-clust0.5.npy") for lib in listlib ]
Nres = len(libraries)
Nchains = len(chains)

atoms = [0] # first atom in each residue
for lib in libraries:
    atoms.append(atoms[-1]+lib.shape[1])

print atoms
print chains.shape
monomers_chains = [ chains[:, atoms[i]:atoms[i+1] ,:] for i in range(Nres) ]

r = range(Nres)
if args.noext:
    r = r[1:-1]

print chains.shape
j=1
for i in r:
    monomer = chains[j, atoms[i]:atoms[i+1],:]
    fitted, RMSD = fit_multi_npy(libraries[i], monomer)
    best = fitted[ RMSD.argmin(axis=0)]
    print "best.shape", best.shape
    print chains[j, atoms[i]:atoms[i+1],:].shape
    print atoms[i], atoms[i+1]
    for k in range(atoms[i], atoms[i+1]):
        chains[j, k,:] = best[k-atoms[i],:]

print chains.shape
np.save(args.aa_npy, chains[0][None,:,:])
