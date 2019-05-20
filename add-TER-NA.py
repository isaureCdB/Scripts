#!/usr/bin/python2.7

import sys

P = [0,0,0]
O = [0,0,0]
exresid = 0
for l in open(sys.argv[1]).readlines():
    if l.startswith("TER"):
        ter = True
    if not l.startswith('ATOM') and not l.startswith('HETATM'):
        print l
        continue
    resid = int(l[22:26])
    if resid != exresid
        firstat = True
        headchain = False
        exresid = resid
        if resid != resid+1:
            headchain = True
    if l[12:16].strip() == "O5'" and firstat:
        headchain = True
    if l[12:16].strip() == 'P':
        P = [float(i) for i in l[30:54].split()]
        if sum( [(P[i] - O[i])**2 for i in range(3) ])**0.5 > 2:
            headchain = True
    if l[12:16].strip() in ['P', 'O1P', 'O2P'] and headchain:
        continue
    if l[12:16].strip() == "O3'":
        O = [float(i) for i in l[30:54].split()]
    if headchain and not ter:
        print "TER"
        ter = True
    print l
    ter = False
    firstat = False
