import sys
import numpy
from math import *

inputfile = sys.argv[1]
outputfile = sys.argv[2]

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
  
def write_pdb(outputfile, lines, atoms, extralines):
  print outputfile
  outp = open(outputfile, "w")
  count = 0
  pos = 0
  data = zip(lines, atoms)
  while 1:
    while pos < len(extralines):
      p,d = extralines[pos]
      if count < p: break
      print >> outp, d.rstrip("\n")
      pos += 1
    if count == len(data): break
    l,a = data[count]
    ll = l[:30] + "%8.3f%8.3f%8.3f" % (a[0],a[1],a[2]) + l[54:].rstrip("\n")
    print >> outp, ll
    count += 1
  outp.close()

#read atoms  
lines1, atoms1, extralines1 = read_multi_pdb(inputfile)

at1 = numpy.mean(atoms1, axis=0)

write_pdb(outputfile,lines1, at1, extralines1)





