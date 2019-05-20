#!/usr/bin/python
import sys
from math import sqrt

def correlate(l):
  sumx,sumy,sumxx,sumyy,sumxy = 0,0,0,0,0
  n = len(l)
  for ll in l:
    x = float(ll[0])
    y = float(ll[1])
    sumx += x
    sumy += y
    sumxx += x * x
    sumyy += y * y
    sumxy += x * y
  Sxx = sumxx - sumx * sumx/ n
  Sxy = sumxy - sumx * sumy/ n
  Syy = sumyy - sumy * sumy/ n
  r = Sxy/sqrt(Sxx * Syy)
  return r  

d = []
for l in sys.stdin.readlines(): d.append(l.split())
  
print correlate(d)
