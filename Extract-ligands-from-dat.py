#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
#################################################
DAT=open(sys.argv[1],'r')
OUT=open(sys.argv[2],'w')
Nlig = int(sys.argv[3])
ligandlist = sys.argv[4:]
#################################################
L=DAT.readlines()
dat=L
deb=0
LEN=len(dat)
i=0
while i < LEN:
	l=L[i].split()
	if l[0]=='#pivot':
		for j in ligandlist:
			OUT.write(dat[int(i)+int(j)-1]) 
		i+=Nlig
	line=list(dat[i])
	if line[0]=='#':
		OUT.write(dat[i])
		i+=1
	else:
		for j in ligandlist:
			OUT.write(dat[int(i)+int(j)-1]) 
		i+=Nlig

DAT.close()
OUT.close()
