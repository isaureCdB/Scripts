#!/usr/bin/env python3
import sys

chains = open(sys.argv[1]).readlines()
clashing = set([int(l.split()[0])-1 for l in open(sys.argv[2]).readlines()])

for nc, c in enumerate(chains):
    if nc not in clashing:
        print(c, end=' ')
