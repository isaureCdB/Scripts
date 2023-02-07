#!/usr/bin/env python3

import numpy as np
import sys, argparse
import itertools

'''
usage: python dat2npy.py <file.dat>
convert a file.dat into a np.array of (energy), (conformer) and rotation-tranlation matrices
WARNING: must have fixed receptor (first rot-trans line of each pose is all zeros)
'''
########################
parser =argparse.ArgumentParser(description=__doc__,
						formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat', help="structures in ATTRACT format")
parser.add_argument('--score', help="input scores file")
parser.add_argument('--npz', action='store_true')
parser.add_argument('--maxposes', help='size of presaved np.array, default 10**6')
args = parser.parse_args()
########################

max_nposes = 10000000
if args.maxposes:
	max_nposes = int(args.maxposes)

datfile = args.dat

npy = np.zeros((max_nposes,6), dtype=float)
ene = np.zeros(max_nposes, dtype=float)
ens = np.zeros(max_nposes, dtype=np.int32)
fix_rec = False
energies = False
ensemble = False
headers = []
pivots = []

i=-1
for l in open(datfile).readlines():
	l = l.rstrip("\n")   
	if len(l.split()) == 1:
		i += 1
	if i == -1:
		headers.append(l)
		continue
	if l.startswith("#pivot"):
		p = [float(i) for i in l.split()[2:]]
		pivots.append(p)
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

if args.score:
	ss=open(args.score).readlines()
	ll = [l.split() for l in open(args.score).readlines()]
	scores = [ float(l[1]) for l in ll if l[0]=="Energy:"]
	ene = np.array(scores)
 
if args.npz:
	outp1 = datfile + ".npz"
	npz = {}
	npz['coor'] = npy[:i]
	npz['conformers'] = ens[:i]
	npz['pivots'] = np.array(pivots)
	npz['energy'] = ene[:i]
	np.savez(outp1, **npz)	

else:
	outp1 = datfile + ".npy"
	outp2 = datfile + ".ene"
	outp3 = datfile + ".ens"
	outp4 = open(datfile + ".header", 'w')
	
	for l in headers:
		print(l, file=outp4)
	outp4.close()

	np.save(outp1, npy[:i+1])
	if energies:
		np.save(outp2, ene[:i+1])
	if ensemble:
		np.save(outp3, ens[:i+1])
