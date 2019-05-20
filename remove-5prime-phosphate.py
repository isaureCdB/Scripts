#!/usr/bin/python2.7

import sys

P = [0,0,0]
O = [0,0,0]
exresid = 0
deb = True
for l in open(sys.argv[1]).readlines():
    if not l.startswith('ATOM') and not l.startswith('HETATM'):
        continue
    resid = int(l[22:26])
    if resid != exresid:
        firstat = True
        headchain = False
        if resid != exresid+1:
            headchain = True
        exresid = resid
    if l[12:16].strip() != "P" and firstat:
        headchain = True
    if l[12:16].strip() == 'P':
        P = [float(i) for i in l[30:54].split()]
        if sum( [(P[i] - O[i])**2 for i in range(3) ])**0.5 > 2:
            headchain = True
    if headchain and firstat and not deb:
            print "TER"
    if l[12:16].strip() in ['P', 'O1P', 'O2P'] and headchain:
        firstat = False
        continue
    if l[12:16].strip() == "O3'":
        O = [float(i) for i in l[30:54].split()]
    nres = l[17:21].strip()[:2]+" "
    if headchain:
        nres = nres[:2]+"5"
    l = l[:17] + nres + l[20:]
    print l,
    firstat = False
    deb = False
