#!/usr/bin/env python2
import sys
from _read_struc import read_struc

def write_structure(struct, n):
    l1,l2 = struct
    print "#"+str(n)
    try:
        for l in l1: print l
        for l in l2: print l
    except IOError:
        sys.exit()

header,structures = read_struc(sys.argv[1])

for h in header: print h

d_sorted = {}
n = 0
for ns, s in enumerate(structures):
    l1,l2 = s
    ind = [l.split()[1] for l in l1 if l.split()[3]=="sort"]][0]
    d_sorted[ind] = s

indices = list(d_sorted.keys()).sort()

for ni,i in enumerate(indices):
    write_structure(d_sorted[i], ni)
