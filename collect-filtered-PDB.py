#/bin/python

import os
import sys

P = [line.rstrip() for line in open(sys.argv[1])]
I = [line.rstrip() for line in open(sys.argv[2])]
L = [line.rstrip() for line in open(sys.argv[3])]

pdb=open('filtered.pdb','w')

for j in range(len(I)):
	for p in range(len(P)):
		pdb.write('%s\n'%P[p])
	i=int(I[j])-1
	r=i*37+1
	s=r+36
	pdb.write('TER\n')
	for l in range(r,s):
		pdb.write('%s\n'%L[l])
	pdb.write('ENDMDL\n')




