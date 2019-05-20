#!/usr/bin/env python2

from __future__ import print_function
import sys
from math import *
from _read_struc import read_struc
import random, numpy as np

print ("Usage: ensemblize <DOF file> <boolean matrix><clusterfile>", file = sys.stderr)

header,structures = read_struc(sys.argv[1])
matrix = np.load(sys.argv[2])
clustfile = sys.argv[3]

clusters = [ l.split()[3:] for l in open(clustfile).readlines()]

stnr = 1
for h in header: print(h)
for ns, s in enumerate(structures):
    l1, l2 = s
    col = matrix[ns]
    for nclust, clust in enumerate(clusters):
        if col[nclust]:
            for c in clust:
                print("#"+str(stnr))
                for l in l1:
                    print(l)
                print(l2[0])
                print(c + " " + " ".join(l2[1].split())),
                stnr += 1

assert len(matrix) == ns+1, (len(matrix), ns+1)
