#!/usr/bin/env python3

import sys

clust = sys.argv[1]
indices = [ l.split() for l in open(sys.argv[2]).readlines()]
mapping = {ind[0] : ind[1] for ind in indices}

for nl, l in enumerate(open(clust).readlines()):
    old = l.split()[3:]
    print('cluster %s =>'%str(nl+1), end=' ')
    for i in old:
        ii = mapping[i]
        print(ii, end=' ')
    print('')
