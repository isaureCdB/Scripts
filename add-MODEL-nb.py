#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os
f=open(sys.argv[1],'r')
g=open('MODEL-'+sys.argv[1],'w')
p=f.readlines()
P=p
r=0
struct=1
i=0
g.write('MODEL   '+str(struct)+'\n')
for line in P[:-1]:
#	if line.startswith('ATOM') or line.startswith('TER') :g.write(line)
	if line.startswith('ATOM') :g.write(line)
	elif line.startswith('END'):
		struct+=1
		g.write('ENDMDL\n')
		g.write('MODEL   '+str(struct)+'\n')

g.write('ENDMDL')
g.close()
