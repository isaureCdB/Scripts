#!/usr/bin/env python3

import numpy as np, sys, argparse
'''
usage: npy2dat file.dat.header file.dat.npy --ens file.dat.ens --ene file.dat.ene > file.dat
reverse process from "dat2npy.py"
'''

#######################
parser = argparse.ArgumentParser(description=__doc__,
						formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('coor')
parser.add_argument('header')
parser.add_argument("--ens",help="ensemble conformer")
parser.add_argument("--ene",help="energies")
args = parser.parse_args()
#######################

header = open(args.header).readlines()
for l in header:
    print(l, end='')

coor = np.load(args.coor)
print(coor.shape, file=sys.stderr)
if args.ene is not None:
	ene =  np.load(args.ene)

if args.ens is not None:
	ens =  np.load(args.ens)

print(ens, file=sys.stderr)
nstruc = len(coor)

for s in range(nstruc):
	print("#%i"%(s+1))
	if args.ene is not None:
		print("## Energy: %.3f"%ene[s])
	print(" 0 0 0 0 0 0")
	if args.ens is not None:
		print(" %s"%ens[s], end=" ")
	for j in coor[s][:-1]:
		print(" %.4f"%j, end=' ')
	print(" %.4f"%coor[s][-1])
