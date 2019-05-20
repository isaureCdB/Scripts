#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
import os

#################################################
def run(command):
  sys.stdout.flush()
  os.system(command)
#################################################
run('mkdir '+sys.argv[1])

lib=open(sys.argv[1]+'.pdb','r').readlines()
pdb=lib
conf=1
C=open(sys.argv[1]+'/'+sys.argv[2]+'1.pdb','w')
for l in pdb[:-1]:
	if not l.startswith('ATOM'):
		conf+=1
		C.close()
		C=open(sys.argv[1]+'/'+sys.argv[2]+str(conf)+'.pdb','w')
	else:C.write(l)
