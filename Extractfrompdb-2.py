#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os
#################################################
def run(command):
  sys.stdout.flush()
  os.system(command)
#################################################
Rank=[int(r) for r in sys.argv[2:]]
f=open(sys.argv[1]+'.pdb','r')

p=f.readlines()
P=p

i=0
while i in range(len(P)):
	if P[i].split()[0]=='END' or P[i].split()[0]=='ENDMDL' :
		j=i+1
		break
	i+=1

for r in Rank:
	deb=j*(r-1)+1
	fin=deb+j-1
	run('sed -n "'+str(deb)+','+str(fin)+'p" '+sys.argv[1]+'.pdb > '+sys.argv[1]+'-rk'+str(r)+'.pdb')

