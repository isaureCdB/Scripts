origins = [[0,0,0],[0,0,0],[0,0,0],]
import sys
import os
args = sys.argv[1:]

sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc
import random
from math import *

header,structures = read_struc(args[0])

for h in header: print h
stnr = 0
for s in structures:
  stnr += 1
  l1,l2 = s
  oris = []
  for lnr in range(len(l2)):
    l = l2[lnr]
    ori = [float(v) for v in l.split()[3:6]]  
    oris.append(ori)
  dsq = []
  for i in oris:
    ddsq = []
    for j in origins:
      d = sum([(ii-jj)**2 for ii,jj in zip(i,j)])
      ddsq.append(d)
    dsq.append(ddsq)

  orderdic = {}
  for n in range(len(oris)):
    mindis = 99999999999
    minorigin = None
    minori = None
    for i in range(len(oris)):
      if i in orderdic.values(): continue      
      ddsq = dsq[i]
      for ii in range(len(origins)):
        if ii in orderdic.keys(): continue
        if ddsq[ii] < mindis: 
          mindis = ddsq[ii]
          minorigin = ii
          minori = i
    orderdic[minorigin] = minori
  
  order = []
  for i in range(len(origins)):        
    order.append(orderdic[i])
  print "#"+str(stnr)
  for l in l1: print l
  for lnr in order: 
    l = l2[lnr]
    print l

