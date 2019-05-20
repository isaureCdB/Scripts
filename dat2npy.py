#!/usr/bin/env python2

import numpy as np
import sys
from _read_struc import read_struc
'''
usage: python dat2npy.py <file.dat>
convert a file.dat into a np.array of (energy), (conformer) and rotation-tranlation matrices
WARNING: must have fixed receptor (first rot-trans line of each pose is all zeros)
'''
datfile = sys.argv[1]

max_nposes = 10000000
if len(sys.argv) > 2:
    max_nposes = int(sys.argv[2])

outp1 = datfile + ".npy"
outp2 = open(datfile + ".ene", 'w')
outp3 = open(datfile + ".ens", 'w')
outp4 = open(datfile + ".header", 'w')

header,structures = read_struc(datfile)

for l in header:
    print >> outp4 , l
outp4.close()

npy = np.zeros((max_nposes,6), dtype=float)
ene = np.zeros(max_nposes, dtype=float)
energies = False
ensemble = False
i=0
for (l1, l2) in structures:
    if i==0:
        if len(l2[1].split()) == 7:
            ens = np.zeros(max_nposes, dtype=np.int32)
            ensemble = True
    try:
        ene[i] = [ float(l[10:]) for l in l1 if l.startswith("## Energy:")][0]
        energies = True
    except:
        pass
    if ensemble:
        ens[i] = int(l2[1].split()[0])
        npy[i] = [ float(j) for j in l2[1].split()[1:]]
    else:
        npy[i] = [ float(j) for j in l2[1].split()]
    i += 1

npy = npy[:i]
np.save(outp1, npy)

if energies:
    ene = ene[:i]
    np.save(outp2, ene)
if ensemble:
    ens = ens[:i]
    np.save(outp3, ens)
