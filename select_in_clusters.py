#!/usr/bin/env python3

import sys
clusters = [ i for i in open(sys.argv[1]).readlines()]
n = int(sys.argv[2])

for l in clusters:
    ll = l.split()[3:]
    m = min(n, len(ll))
    for i in range(m):
        print(ll[i])
