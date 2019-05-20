#!/usr/bin/python2.7
import sys
import os

f=open(sys.argv[1],'r')
deb=1
if len(sys.argv) > 2:
    deb=int(sys.argv[2])
resdeb=0
if len(sys.argv) > 2:
    resdeb=int(sys.argv[3])-1

pdb=f.readlines()

prev = None
res = resdeb
for at, l in enumerate(pdb):
    if l[23:26] != prev:
        prev = l[23:26]
        res += 1
    print l[:7]+"%4d"%(at+deb)+l[11:23]+"%3d"%res+l[26:],

