#!/usr/bin/python2.7

import sys
import os

def run(command):
  sys.stdout.flush()
  os.system(command)

phsug=["P","O1P","OP1","O2P","OP2","O3P","OP3","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"]
revpho=["C5'","O5'","P","O1P","OP1","O2P","OP2"]
phsugPu=phsug + ["N9","C8","N7","C5","C6"]

Order={
'2MG':phsugPu+["O6","N1","C2","N2","CM2","N3","C4"],
'H2U':phsug+["N1","C2","O2","N3","C4","O4","C5","C6"],
'M2G':phsugPu+["O6","N1","C2","N2","N3","C4","CM1","CM2"],
'OMC':["N1","C2","N3","C4","C5","C6","O2","N4","C1'","C2'","O2'","CM2","C3'","C4'","O4'","O3'"]+revpho,
'CM9':["N1","C2","N3","C4","C5","C6","O2","N4","C1'","C2'","O2'","CM2","C3'","C4'","O4'","O3'"]+revpho,
'OMG':["P","O1P","OP1","O2P","OP2","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","CM2","C1'","N9","C8","N7","C5","C6","O6","N1","C2","N2","N3","C4"],
'YG':["N1","N2","C2","N3","C3","C4","C5","C6","O6","N7","C8","N9","C10","C11","C12","C13","C14","C15","C16","O17","O18","C19","N20","C21","O22","O23","C24","C1'","C2'","O2'","C3'","O3'","C4'","O4'"]+revpho,
'PSU':["N1","C2","N3","C4","C5","C6","O2","O4","C1'","C2'","O2'","C3'","C4'","O3'","O4'"]+revpho,
'5MC':phsug+["N1","C2","O2","N3","C4","N4","C5","C6","CM5"],
'7MG':phsugPu+["O6","N1","C2","N2","N3","C4","CM7"],
'5MU':["N1","C2","N3","C4","C5","C5M","C6","O2","O4","C1'","C2'","O2'","C3'","C4'","O3'","O4'"]+revpho,
'1MA':phsugPu+["N6","N1","CM1","C2","N3","C4"],
}

Order.update(dict.fromkeys(['A', 'DA','RA', 'DA5','DA3','A3','A5','ADE'],phsugPu+["N6","N1","C2","N3","C4"]))
Order.update(dict.fromkeys(['G', 'DG','RG', 'DG5','DG3','G5','G3','GUA'],phsugPu+["N6","O6","N1","C2","N2","N3","C4"]))
Order.update(dict.fromkeys(['C', 'DC','RC', 'DC5','DC3','C3','C5','CYT'],phsug+["N1","C2","O2","N3","C4","N4","C5","C6"]))
Order.update(dict.fromkeys(['T', 'DT','DT5','DT3','T3','T5','THY'],phsug+["N1","C2","O2","N3","C4","O4","C5","C7","C6"]))
Order.update(dict.fromkeys(['U','URA','RU','URI','U5','U3'],phsug+["N1","C2","O2","N3","C4","O4","N4","C5","C6"]))

#################################################
f=open(sys.argv[1],'r')
g=open('reorder-'+sys.argv[1],'w')
pdb=f.readlines()

def reorder(res):
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
		if len(res)>1: reorder(res)
		g.write(pdb[p])
		p+=1
		previous=0
		res=[]
		continue
 	resid=pdb[p][21:26]
        if resid!=previous and previous!=0:
		reorder(res)
		res=[]
	res.append(pdb[p])
	previous=resid
	p+=1

if len(res)>1: reorder(res)

g.close()
