"""
Calculate averaged structure from several PDB files
usage: python averstruct.py <1.pdb> <2.pdb> [<3.pdb> ...]  [--output <file>]

--allatoms: use all atoms rather than backbone atoms

"""

import sys
from math import sqrt
import numpy

anr = 0
output = None
while 1:
  anr += 1
      
  if anr > len(sys.argv)-1: break  
  arg = sys.argv[anr]
    
  if anr <= len(sys.argv)-2 and arg == "--output":
    output = sys.argv[anr+1]
    sys.argv = sys.argv[:anr] + sys.argv[anr+2:]
    anr -= 2
    continue
    
  if arg.startswith("--"): raise Exception("Unknown option '%s'" % arg)

if len(sys.argv) < 3:
  raise Exception("Please supply PDB files")
 
out = sys.stdout
if output is not None:
  out = open(output,'w')

PDB=sys.argv[1:]
print PDB

def get_atoms(f):
  L=[]
  for l in open(f):
    if not l.startswith("ATOM"): continue
    L.append(l)
  return L

L=[get_atoms(pdb) for pdb in PDB]
for j in range(1,len(L)):
  assert len(L[j]) == len(L[0]), (len(L[j]), len(L[0]))

for l in range(len(L[0])):
  x=numpy.mean([float(G[l][30:38]) for G in L ])
  y=numpy.mean([float(G[l][38:46]) for G in L ])
  z=numpy.mean([float(G[l][46:54]) for G in L ])
  a,b,c='%.3f'%(x),'%.3f'%(y),'%.3f'%(z)
  out.write(L[0][l][0:30])
  for r in range(8-len(a)):out.write(' ')
  out.write(a)
  for r in range(8-len(b)):out.write(' ')
  out.write(b)
  for r in range(8-len(c)):out.write(' ')
  out.write(c)
  out.write(L[0][l][54:])
  
out.close()
