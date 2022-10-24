#!/usr/bin/env python3

import numpy as np
import sys
import itertools

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
outp2 = datfile + ".ene"
outp3 = datfile + ".ens"
outp4 = open(datfile + ".header", 'w')

npy = np.zeros((max_nposes,6), dtype=float)
ene = np.zeros(max_nposes, dtype=float)
ens = np.zeros(max_nposes, dtype=np.int32)
fix_rec = False
energies = False
ensemble = False

i=-1
for l in open(datfile).readlines():
	l = l.rstrip("\n")   
	if len(l.split()) == 1:
	    i += 1
	if i == -1:
		print(l, file=outp4)
		continue
	if l.startswith("## Energy"):## Energy:
		energies = True
		ene[i] = float(l[10:])
	if not l.startswith("#"):
		if not fix_rec:
			assert len([ll for ll in l.split() if float(ll)==0]) == 6, "receptor not fixed"
			fix_rec = True
		if len(l.split()) == 7:
			ensemble = True
			ens[i] = int(l.split()[0])
			npy[i] = [ float(j) for j in l.split()[1:]]
		if len(l.split()) == 6:
			npy[i] = [ float(j) for j in l.split()]

outp4.close()

npy = npy[:i]
np.save(outp1, npy)

if energies:
    ene = ene[:i]
    np.save(outp2, ene)
if ensemble:
    ens = ens[:i]
    np.save(outp3, ens)
