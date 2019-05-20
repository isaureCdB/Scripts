import sys
pdb = sys.argv[1]
atomindex1 = int(sys.argv[2])
atomindex2 = int(sys.argv[3])
from math import sqrt

firstmodelsize = None
modelsize = 0
coor1 = None
coor2 = None
for l in open(pdb).readlines():
  if not l.startswith("ATOM"): continue
  modelsize += 1
  if modelsize == atomindex1:
    x = float(l[30:38])
    y = float(l[38:46])
    z = float(l[46:54])
    coor1 = x,y,z
  if modelsize == atomindex2:
    x = float(l[30:38])
    y = float(l[38:46])
    z = float(l[46:54])
    coor2 = x,y,z

c1, c2 = coor1, coor2
d = c1[0]-c2[0], c1[1]-c2[1], c1[2]-c2[2]
print sqrt(d[0]**2+d[1]**2+d[2]**2)
