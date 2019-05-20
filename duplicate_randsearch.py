#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
#################################################
Nlig = int(sys.argv[3])
OUT=open(sys.argv[2],'w')
DAT=open(sys.argv[1],'r')
#################################################
L=DAT.readlines()
dat=L
deb=0
LEN=len(dat)
i=0
while i < LEN:
	OUT.write(dat[i]) 
	l=L[i].split()
	i+=1	
	if l[0]=='#pivot' and l[1]=='2':
		for j in range(Nlig):OUT.write('#pivot %i %j %k %l\n'%(j+3,l[2],l[3],l[4]))
		break
	if l[0]=='#pivot' and l[1]=='auto':
		OUT.write(L[i])
		break
i+=1
while i < LEN:
	line=list(dat[i])
	if line[0]=='#':
		OUT.write(dat[i]) 
		i+=1
	else:
		OUT.write(dat[i])
		for j in range(Nlig):OUT.write(dat[i+1]) 
		i+=2

DAT.close()
OUT.close()
