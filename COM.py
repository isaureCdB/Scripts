#!/usr/bin/env python3

import sys

def proceed(coor):
    n = len(coor)
    COM = [ sum([coor[i][j] for i in range(n) ])/n for j in range(3) ]
    roundCOM = [ round(COM[i]*1000)/1000 for i in range(3) ]
    allcoor = [j**2 for c in coor for j in c ]
    gyr = ( sum(allcoor)/n )**0.5
    print("COM: ", roundCOM[0], roundCOM[1], roundCOM[2], file=sys.stderr)
    print("gyr: %.2f"%gyr, file=sys.stderr)
    print(t[:30]+"%8.3f%8.3f%8.3f"%(COM[0], COM[1], COM[2])+t[54:-1])



coor = []
for l in open(sys.argv[1]).readlines():
    if l.startswith("MODEL"):
        print(l, end="")
    if l.startswith("END"):
        if len(coor) > 0:
            proceed(coor)
        coor = []
    if not l.startswith("ATOM"):
        continue
    t = l
    coor.append([float(l[30:38]),float(l[38:46]),float(l[46:54])])

if len(coor) > 0:
    proceed(coor)
