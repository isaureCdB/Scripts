#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os

atdeb=sys.argv[2]
resdeb=int(sys.argv[3])-1
at=int(atdeb)
res=int(resdeb)
f=open(sys.argv[1],'r')
g=open('renum-'+sys.argv[1],'w')
pdb=f.readlines()
#################################################
def write(line,g,at):
	g.write('ATOM')
	for i in range(7-len(str(at).strip())):
		g.write(' ')
	g.write('%i'%at)
	for i in line[11:20]: g.write('%s'%i)		#atname - resname
	for i in range(6-len(str(res).strip())): g.write(' ')
	g.write('%s'%str(res))					#res number
	for i in line[26:]: g.write('%s'%i)		#end of line
#################################################
for line in pdb:
	p=line.split()
#	if p[0]=='ENDMDL' or p[0]=='TER':
	if p[0]=='ENDMDL':
		g.write(p[0]+'\n')
		at=int(atdeb)
		res=int(resdeb)
		continue
	if p[0]!='ATOM':
		g.write('%s'%line)
	else:
		if p[2]=='GP1' or p[2]=='N': res+=1
		write(line,g,at)
		at+=1

g.close()
f.close()
#os.system('rm '+PDB+'.pdb','r')
