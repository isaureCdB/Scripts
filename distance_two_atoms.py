#!/usr/bin/env python3
import sys
import numpy
from math import *

struct1 = sys.argv[1]   # pdb file
atom1 = int(sys.argv[2]) # ATOM index starting from 1
struct2 = sys.argv[3]
atom2 = int(sys.argv[4])

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

#read atoms
lines1, atoms1, extralines1 = read_pdb(struct1)
lines2, atoms2, extralines2 = read_pdb(struct2)

at1 = atoms1[atom1-1]
at2 = atoms2[atom2-1]

d = (at1-at2)**2
print(sum(d)**0.5)
