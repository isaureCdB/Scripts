#!/usr/bin/python2.7

import sys
import os
import numpy

def read_multi_pdb(f):
  Lines=[[]]
  lines=Lines[-1]
  endmodel = False
  allcoor = [[]]
  coor = allcoor[-1]
  for l in open(f):
    if l.startswith("ENDMDL"):      
      endmodel = True
      allcoor = [coor for coor in allcoor if len(coor)]
      Lines=[lines for lines in Lines if len(lines)]
      yield allcoor,Lines 
      allcoor = [[]]
      coor = allcoor[-1]
      Lines=[[]]
      lines=Lines[-1]
    if not l.startswith("ATOM"): continue
    coo = [float(f) for f in (l[30:38],l[38:46],l[46:54])]
    lines.append(l)
    coor.append(coo)
    endmodel = False
  allcoor = [coor for coor in allcoor if len(coor)]
  Lines=[lines for lines in Lines if len(lines)]
  if not endmodel: yield allcoor,Lines 

M=open('origin-'+sys.argv[1],'w')

for allcoor,Lines in read_multi_pdb(sys.argv[1]):
	X,Y,Z=sum([c[0] for c in allcoor[0]])/len(allcoor[0]),sum([c[1] for c in allcoor[0]])/len(allcoor[0]),sum([c[2] for c in allcoor[0]])/len(allcoor[0])
	for i in range(len(Lines[0])):
		l=Lines[0][i]
		x,y,z=allcoor[0][i]
		a,b,c='%.3f'%(x-X),'%.3f'%(y-Y),'%.3f'%(z-Z)
#		a,b,c=round(1000*(x-X))/1000,round(1000*(y-Y))/1000,round(1000*(z-Z))/1000
#		M.write(l[0:30]+'{0:8}'.format(a)+'{0:8}'.format(b)+'{0:8}'.format(c)+l[54:])
		M.write(l[0:30])
		for r in range(8-len(a)):M.write(' ')
		M.write(a)
		for r in range(8-len(b)):M.write(' ')
		M.write(b)
		for r in range(8-len(c)):M.write(' ')
		M.write(c)
		M.write(l[54:])
	M.write('ENDMDL\n')
