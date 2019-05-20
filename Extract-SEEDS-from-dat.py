#!/usr/bin/python2.7
###########################
###  L I B R A R I E S  ###
###########################
import sys
#################################################
clusterlist = sys.argv[3:]
OUT=open(sys.argv[2],'w')
DAT=open(sys.argv[1],'r')
#################################################
L=DAT.readlines()
dat=L
deb=0
for l in L:
	line=l.split()
	if len(line)<2:
		deb+=1
		continue
	if line[1]=='SEED':
#		print(line)		
		break
	deb+=1
	OUT.write(l)

l=deb
index=0
seed=0
#print(clusterlist[index])
while l < len(L) and index < len(clusterlist):
	if len(L[l].split())<2:l+=1
	if L[l].split()[1]=='SEED':
#		print('SEED '+str(seed))
		seed+=1
		if seed==int(clusterlist[index]):
			index+=1
			OUT.write('#%i\n'%index)
			while len(L[l].split())>1:
				OUT.write(L[l])  
				l+=1
	l+=1

DAT.close()
OUT.close()
