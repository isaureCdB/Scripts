#!/usr/bin/python2.7
import sys
import os

dat2=open('renum-'+sys.argv[1],'w')
L=open(sys.argv[1],'r').readlines()

i=1
for line in L:
	l=line.strip()
	if line.strip()[0]=='#' and len(line.split())==1:
		try:
			x=int(l[1])
			dat2.write('#%i\n'%i)
			i+=1
			continue		
		except ValueError : pass
	if line.strip()[0]=='#pivot' or line.strip()[0]=='#centered':pass
	dat2.write(line)
	
