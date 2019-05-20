#!/usr/bin/env python
import sys

header = open(sys.argv[1]).readlines()
coor = open(sys.argv[2]).readlines()
score = [ l.split()[0] for l in open(sys.argv[3]).readlines()]

for l in header:
        print l,

for i in range(len(score)):
    print "#%i"%(i+1)
    print "## Energy: %s"%score[i]
    print "   0.0 0.0 0.0 0.0 0.0 0.0"
    print coor[i],
