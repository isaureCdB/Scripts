#!/usr/bin/env python3

import sys

f=sys.argv[1]

m = 0
s = 0
n = 0
for l in open(f).readlines():
    if l.startswith("real"):
        m += int(l.split()[1].split("m")[0])
        s += float(l.split()[1].split("m")[1].split("s")[0])
        n += 1

tots = 60*m + s
m += s//60
s = s%60

aver_tots = tots/n
M = aver_tots//60
S = aver_tots%60


print(" %i m %i s = %i s"%(m,s, tots))
print("aver: %i m %i s = %i"%(M, S, aver_tots))
