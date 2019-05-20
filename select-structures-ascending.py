#!/usr/bin/env python2

import sys
from _read_struc import read_struc
header, structures = read_struc(sys.argv[1])

selstruc = {}
if sys.argv[2] == "-f":
  selected = [int(l.split()[0]) for l in open(sys.argv[3]).readlines()]
else:
  selected = [int(v) for v in sys.argv[2:]]
selected_set = set(selected)

for h in header: print h
s = 0
kept = 0
for struc in structures:
    s+=1
    if s not in selected_set:
        continue
    kept += 1
    l1,l2 = struc
    print "#"+str(kept)
    print "##%d => select" % s
    try:
        for l in l1: print l
        for l in l2: print l
    except IOError:
        sys.exit()
    if kept == len(selected_set):
        break
