#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os
#################################################
pdb=open(sys.argv[1],'r')
pdbout=open('his-'+sys.argv[1],'w')
L=pdb.readlines()
HIP=[]
HIE=[]
#################################################
def changehis(line,etat):
	for i in line[:17]: pdbout.write('%s'%i)
	pdbout.write(etat)
	for i in line[20:]: pdbout.write('%s'%i)
#################################################
for line in L:
	if len(line.split())<4:continue
	if line.split()[3].strip()[0]=='H':
		if line.split()[2]=='N':hd1=0
		if line.split()[2]=='HD1': hd1=1
		if line.split()[2]=='HE2':
			if hd1==1:HIP.append(line.split()[4])
			else:HIE.append(line.split()[4])

for line in L:
	if len(line.split())<4:
		pdbout.write('%s'%line)
		continue
	if line.split()[3].strip()[0]=='H':
		hid=True
		for res in HIP:
			if line.split()[4]==res:
				changehis(line,'HIP')
				hid=False
		for res in HIE:
			if line.split()[4]==res:
				changehis(line,'HIE')
				hid=False
		if hid is True: changehis(line,'HID')
	else:
		for i in line[:17]+line[17:]:pdbout.write('%s'%i)

pdbout.close()
