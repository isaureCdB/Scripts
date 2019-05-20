#!/usr/bin/env python3

import sys

superclustfile = sys.argv[1]
clustfile = sys.argv[2]

superclust = { l.split()[0] : l.split()[1] for l in open(superclustfile).readlines()}

for l in open(clustfile).readlines():
    ll = l.split()
    print(ll[0], superclust[ll[1]])
