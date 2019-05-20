#!/usr/bin/python2.7
import sys

pdb = open(sys.argv[1], "r").readlines()
vect = [ float(i) for i in sys.argv[2:5] ]

for l in pdb:
    if len(l) < 53:
        print l
        continue
    x = float(l[30:38])
    y = float(l[39:46])
    z = float(l[47:54])
    print l[:30]+"%8.3f%8.3f%8.3f"%(x+vect[0], y+vect[1], z+vect[2])+l[54:],

