#!/usr/bin/env python3

import sys, argparse
import numpy as np
from rmsdlib import multifit

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

def pdb2npy(pdb):
    coord = []
    for l in open(pdb).readlines():
        if l.startswith("MODEL") or len(coord) == 0:
            coord.append([])
        if not l.startswith("ATOM"):
            continue
        coord[-1].append([ float(i) for i in [l[30:38], l[38:46], l[46:54]] ] )
    return np.array(coord)

def fit_multi_npy_part(a, ref, atoms):
    ref_fit = ref[atoms]
    a_fit = npy[:,atoms]
    rotation, translation, RMSD = multifit(a_fit, ref_fit)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a_fit.sum(axis=1)/a_fit.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik', centered, rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

'''
    rotmats, offsets, rmsds = multifit(a_fit, ref_fit)
    rotmats = rotmats.swapaxes(1,2)
    offsets = -offsets
    x = rmsds.argsort()
    pivots = a_fit.sum(axis=1)/a_fit.shape[1]
'''

def fit_multi_npy(a, ref):
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a.sum(axis=1)/a.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('npy', help="np array")
parser.add_argument('outp_npy', type=str, default = None)
parser.add_argument('--rmsd', type=str, default = None)
parser.add_argument('--pdb', type=str, default = None)
parser.add_argument("--npyref", type=str, default = None)
parser.add_argument("--atoms", type=str, nargs='+', default = None)
parser.add_argument("--first", action="store_true")
args = parser.parse_args()
############
npy = np.load(args.npy)
#print(args.pdb)

if args.pdb != None:
    ref = pdb2npy(args.pdb)[0]
elif args.npyref != None:
    print("ref is npy")
    ref = npy2to3(np.load(args.npyref))
elif args.first:
    ref = npy[0]
else:
    raise Exception("no reference provided")

if len(npy.shape)==2:
    assert npy.shape[1] == 3
    npy = npy[None,:]

if len(ref.shape)==3:
    assert ref.shape[2] == 3 and ref.shape[0] == 1
    ref = ref[0]

if args.atoms:
    atoms = [int(i)-1 for i in args.atoms]
    new_npy, rmsd = fit_multi_npy_part(npy, ref, atoms)
else:
    new_npy, rmsd = fit_multi_npy(npy, ref)

if args.rmsd != None:
    f=open(args.rmsd,'w')
    for nr, r in enumerate(rmsd):
        print("%i %.3f"%(nr+1, r),file=f)
    f.close()

np.save(args.outp_npy, new_npy)
