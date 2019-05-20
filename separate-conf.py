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
filename=sys.argv[1]+'/'+sys.argv[2]+'1.pdb'
C=None
for l in pdb[:-1]:
  if l.startswith('ENDMDL'):
    conf+=1
    C.close()
    C=None
    filename=sys.argv[1]+'/'+sys.argv[2]+str(conf)+'.pdb'		
  elif l.startswith('ATOM'):
    if C is None:
      print filename
      C=open(filename,'w')
    C.write(l)
