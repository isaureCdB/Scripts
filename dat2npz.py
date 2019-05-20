#!/usr/bin/env python2

import numpy as np
import sys
from _read_struc import read_struc

'''
usage: python dat2npz.py <file.dat>
convert a file.dat into a np.array of energy, conformer and rotation-tranlation matrices
WARNING: must have fixed receptor (first rot-trans line of each pose is all zeros)
'''

datfile = sys.argv[1]
outp1 = datfile.split(".dat")[0] + ".npz"

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

npz = {}
npz['conformers'] = conf
npz['pivots'] = np.array(pivots)
npz['energy'] = ene
npz['coor'] = coor
np.savez(outp1, **npz)
