#!/usr/bin/env  python3
import sys

datlist = [l.split()[0] for l in open(sys.argv[1]).readlines()]
conformers = [int(l.split()[0]) for l in open(sys.argv[2]).readlines()]

for l in open(datlist[0]).readlines()[:3]:
    print(l[:-1])

i = 0
count = 1
for nd, dat in enumerate(datlist):
    conf = conformers[nd]
    for l in open(dat).readlines():
        ll = l.split()
        if len(ll) == 6 and l[0] != "#" and not i:
            rec, i = l, 1
            continue
        if len(ll) == 6 and l[0] != "#" and i:
            #print(l, len(ll), file=sys.stderr)
            print(("#%i"%count))
            print((rec[:-1]))
            print(("%s %s"%(conf, l[1:])), end=' ')
            count +=1
            i = 0
