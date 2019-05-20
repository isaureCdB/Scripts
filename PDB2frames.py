#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
import os
import itertools

pdb=sys.argv[1]

count=1
model=0
ter=0
frames = open('frames_%s'%pdb,'w')
frames.write('MODEL 0\n')

for l in open(sys.argv[1],'r'):
	if l.startswith("ATOM"):
 		frames.write('%s'%l)
		continue
	if l.startswith("TER") and ter==1:
		frames.write('ENDMDL\nMODEL %i\n'%count)
		count+=1
		ter=0
		continue
	if l.startswith("TER") and ter==0:
		ter=1
		continue

