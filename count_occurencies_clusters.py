#!/usr/bin/env python3
import sys
clusters = [ [int(i)-1 for i in l.split()[3:] ] for l in open(sys.argv[1]) ]
occurencies = [int(l.split()[0]) for l in open(sys.argv[2]).readlines()]

for clust in clusters:
    print(sum([ occurencies[i] for i in clust ]))
