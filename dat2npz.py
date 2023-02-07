#!/usr/bin/env python3

import numpy as np
import sys
from _read_struc import read_struc
import argparse

'''
usage: python dat2npz.py <file.dat>
same as dat2npy.py but uses read_struc from ATTRACT 
convert a file.dat into a np.array of energy, conformer and rotation-tranlation matrices
WARNING: must have fixed receptor (first rot-trans line of each pose is all zeros)
'''
########################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat', help="structures in ATTRACT format")
parser.add_argument('--score', help="input scores file")
parser.add_argument('--npz', action='store_true')

args = parser.parse_args()
########################

datfile = args.dat

header,structures = read_struc(datfile)
pivots = []
for l in header:
    if l.startswith("#pivot"):
        pivots.append([ float(i) for i in l.split()[2:]])

structures = list(structures)
nposes = len(structures)

coor = np.zeros((nposes,6))
conf = None
ene = None

l1, l2 = structures[0]

if args.score:
    scores = [ float(l.split()[1]) for l in open(args.score).readlines() if l.startswith("Energy:")])
    ene = np.array(scores)
    
else:
    for l in l1:
        if l.startswith("## Energy:"):
            ene = np.zeros((nposes))
            break

if len(l2[1].split()) > 6:
    conf = np.zeros((nposes))

for i, (l1, l2) in enumerate(structures):
    if ene is not None:
        ene[i] = [ float(l[10:].strip()) for l in l1 if l.startswith("## Energy:")][0]
    lig = l2[1].split()
    coor[i] = [ float(j) for j in lig[-6:]]
    if conf is not None:
        conf[i] = int(lig[0])

if args.npz:
    outp1 = datfile.split(".dat")[0] + ".npz"
    npz = {}
    npz['conformers'] = conf
    npz['pivots'] = np.array(pivots)
    npz['energy'] = ene
    npz['coor'] = coor
    np.savez(outp1, **npz)

else:
    outp1 = datfile + ".npy"
    outp2 = datfile + ".ene"
    outp3 = datfile + ".ens"

    np.save(outp1, coor)
    
    if ene:
        ene = ene[:nposes]
        np.save(outp2, ene)
    
    if conf:
        ens = ens[:nposes]
        np.save(outp3, ens)

    outp4 = open(datfile + ".header", 'w') 
    for l in l1:
        print(l, file=outp4)
    outp4.close()
