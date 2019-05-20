#!/usr/bin/python2.7
import sys
import os

f=open(sys.argv[1],'r')
deb=1
if len(sys.argv) > 2:
    deb=int(sys.argv[2])

pdb=f.readlines()

for at, l in enumerate(pdb):
    print l[:7]+"%4d"%(at+deb)+l[11:],

