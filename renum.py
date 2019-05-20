#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os
import string

PDB=sys.argv[1]
#atdeb=sys.argv[2]
#resdeb=int(sys.argv[3])
f=open(PDB,'r')
g=open('renum-'+PDB,'w')
pdb=f.readlines()

#################################################
def write(line,g,at,res):
	p=line.split()
	g.write('ATOM')
	for i in range(7-len(str(at).strip())):
		g.write(' ')
	g.write('%i  '%at)
	g.write('%s'%p[2])		#atom name
	for i in range(4-len(p[2].strip())):
		g.write(' ')
	g.write('%s'%(p[3]))		#res name
	for i in range(8-len(str(res).strip())):
		g.write(' ')
	g.write('%s  '%str(res))		#res number
	g.write(line[28:])
#################################################
previous_res=-1000
previous_letter=0
at=1
res=1
ter=True
bypass=False

for line in pdb:
	p=line.split()
	if p[0]=='TER':
		g.write('TER\n')
		previous_res=-100
		ter=True
		continue				
	if p[0]!='ATOM' or len(p) < 4:
		g.write('TER\n')
		at=1
		res=1
		previous_res=-100
		ter=True
		continue		
###		
	elif p[4].strip()[-1].isalpha():
		current_res=int(p[4].strip()[:-1])
		current_letter=string.uppercase.index(p[4].strip()[-1])
	else:	current_res=int(p[4])
###
	if p[2]=='P' or p[2]=='N':
###	
		if p[4].strip()[-1].isalpha():
			if current_res==previous_res:
				if current_letter!=previous_letter+1 and not ter: g.write('TER\n')
			previous_letter= current_letter
		elif (len(p[4].strip())==4 and len(str(previous_res))!=4) or (len(p[4].strip())!=4 and len(str(previous_res))==4):pass
		elif current_res!=previous_res+1 and previous_res!=-1 and not ter: g.write('TER\n')
###	
		if not ter: res+=1
	elif current_res!=previous_res and previous_res!=-1000:
		if not ter: g.write('TER\n')
		res+=1
	ter=False	
	previous_res=current_res
	write(line,g,at,res)
	at+=1

g.close()
f.close()
#os.system('rm '+PDB+'.pdb','r')
