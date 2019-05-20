#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
import os


##########################################################################################################
def run(command):
  sys.stdout.flush()
  os.system(command)
##########################################################################################################
r=open('reduced.pdb','w')
for l in open(sys.argv[1],'r'):
	if l.startswith("ATOM"):  
		r.write(l)
	else:
		r.close()
		run('/home/ichauvot/attract/bin/reduce_rna reduced.pdb')
		run('cat reducedr.pdb >> reduced-'+sys.argv[1])
		run('echo ENDMDL >>  reduced-'+sys.argv[1])
		r=open('reduced.pdb','w')
