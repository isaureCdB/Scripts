import sys
import numpy
from math import *

reference = sys.argv[1]
inputfile = sys.argv[2]
outputfile = sys.argv[3]

def read_pdb(pdb):
  atoms = []
  lines0 = open(pdb).readlines()
  lines = []
  extralines = []
  for l in lines0:
    if not l.startswith("ATOM"): 
      extralines.append((len(lines), l))
      continue
    x = float(l[30:38])
    y = float(l[38:46])
    z = float(l[46:54])    
    atoms.append((x,y,z))
    lines.append(l)
  return lines, numpy.array(atoms), extralines

def apply_matrix(atoms, pivot, rotmat, trans):
  ret = []  
  for atom in atoms:
    a = atom-pivot
    atom2 = a.dot(rotmat) + pivot + trans
    ret.append(atom2)
  return ret

def read_multi_pdb(pdb):
  lines0 = open(pdb).readlines()
  States = []
  lines = []
  extralines = []  
  writelines = 1
  for l in lines0:
    if l.startswith("ENDMDL"):
      writelines = 0
      States.append(atoms)
    if l.startswith("MODEL"):
      atoms = []
    if not l.startswith("ATOM"): 
      if writelines == 1: 
        extralines.append((len(lines), l))
      continue
    x = float(l[30:38])
    y = float(l[38:46])
    z = float(l[46:54])    
    atoms.append((x,y,z))
    if writelines == 1: 
      lines.append(l)
  return lines, numpy.array(States), extralines

#read atoms  
lines1, atoms1, extralines1 = read_multi_pdb(inputfile)
lines0, atoms0, extralines0 = read_pdb(reference)

d = (atoms1-atoms0)**2
d = numpy.sqrt(d.sum(axis=2))
d = d.transpose()
numpy.savetxt(outputfile,d, fmt='%.1f')

