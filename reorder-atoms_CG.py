#!/usr/bin/python2.7

import sys
import os

def run(command):
  sys.stdout.flush()
  os.system(command)

phsug=['GP1','GS1','GS2','BN']
Order={'A':phsug+['GA1','GA4','GA3','GA2'], 'G':phsug+['GG1','GG4','GG3','GG2'], 'U':phsug+['GU2','GU3','GU1'],'C':phsug+['GC2','GC3','GC1']}

#################################################
f=open(sys.argv[1],'r')
g=open('reorder-'+sys.argv[1],'w')
pdb=f.readlines()

def reorder(res):
#	print(res)
	order=Order[res[0].split()[3]]
	for at in order:
		for r in res:
			if r.split()[2]==at:
				g.write(r)


res=[]
p=0
previous=0
while p<len(pdb):
	if pdb[p].split()[0]!='ATOM':
		print(p)
		if len(res)>0:reorder(res)
		g.write(pdb[p])
		p+=1
		previous=0
		res=[]
		continue
 	if pdb[p].split()[4]!=previous and previous!=0:
		reorder(res)
		res=[]
	res.append(pdb[p])
	previous=pdb[p].split()[4]
	p+=1
reorder(res)
g.close()
