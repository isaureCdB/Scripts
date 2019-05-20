#!/usr/bin/env python3

import sys

lines = []
for l in open(sys.argv[1]).readlines():
    ll = l
    if l[17:20] == "MSE" and l[:6] == "HETATM":
        ll = "ATOM  " + l[6:]
    lines.append(ll)

p = open(sys.argv[1], "w")
for l in lines:
    print(l[:-1], file=p)
p.close()
