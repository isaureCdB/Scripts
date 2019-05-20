#!/usr/bin/env python3

import sys

pdbr = sys.argv[1]
pdbaa = sys.argv[2]

dict_surf = {}
for at in ['N', 'O', 'sc', 'C', 'CA' ]:
    dict_surf[at] = set()

'''
ATOM      1  N   LYS A   2      29.862   8.090   5.627  1.40   1
'''
nres1 = len([l for l in open (pdbaa).readlines() if l[13:15].strip() == "CA"])
nres2 = len([l for l in open (pdbr).readlines() if l[13:15].strip() == "CA"])
assert nres1 == nres2, ('the PDB files have different numbers of residues')

resind = -1
prev = None
sc_access = [0, 0]
for l in open(pdbaa).readlines():
    if not l.startswith('ATOM'):
        continue
    access = int(l[63])
    resname = l[17:20]
    atname = l[13:15].strip()
    resid = int(l[22:26])
    if resid != prev:
        if sc_access[1] >= 0.5*sc_access[0]:
            dict_surf['sc'].add(resind)
        resind += 1
        prev = resid
        sc_access = [0, 0] #N_atom, N_accessible
    if atname in dict_surf.keys() and access:
        dict_surf[atname].add(resind)
    else:
        sc_access[0] += 1
        if access:
            sc_access[1] += 1

if sc_access[1] >= 0.5*sc_access[0]: #map2, best
    dict_surf['sc'].add(resind)

#if sc_access[1] == sc_access[0]:   #map3
#    dict_surf['sc'].add(resind)

#if sc_access[1] > 0:               #map4
#    dict_surf['sc'].add(resind)

if len(sys.argv) > 3:
    outp = open(sys.argv[3], 'w')
else:
    #outp = open(pdbr.split('.pdb')[0] + '_access.pdb', 'w')
    outp = sys.stdout

i = 0
resind = -1
prev = None
for l in open(pdbr).readlines():
    if not l.startswith('ATOM'):
        continue
    i+=1
    if l[57:59] == '99':
        print(l[:61] + '  0',file=outp),
        continue
    resname = l[17:20]
    atname = l[13:15].strip()
    resid = int(l[22:26])
    if resid != prev:
        resind += 1
        prev = resid
    at = 'sc'
    acc = '0'
    if atname in dict_surf.keys():
        at = atname
    if resind in dict_surf[at]:
        #print(i,file=sys.stderr)
        acc = '1'
    l = l[:61] + '  ' + acc
    print(l, file=outp)


outp.close()
