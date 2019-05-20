#!/usr/bin/env python3
import sys

dat = open(sys.argv[1]).readlines()
clustlines = [ l.split() for l in open(sys.argv[2]).readlines()]
clust = { nc: l[3:] for nc, l in enumerate(clustlines)}

for l in dat:
    if l == "#1":
        break
    print(l[:-1])

count = 1
for l in dat:
    ll = l.split()
    if len(ll) == 6 and l[0] != "#":
        rec = l
    if len(ll) == 7 and l[0] != "#":
        #print(l, len(ll), file=sys.stderr)
        cl = int(l.split()[0])
        for i in clust[cl-1]:
            print("#%i"%count)
            print(rec[:-1])
            print("%s %s %s %s %s %s %s"%(i, ll[1], ll[2],ll[3], ll[4], ll[5], ll[6]))
            count +=1
