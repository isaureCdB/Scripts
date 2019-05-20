#!/usr/bin/env python3

import sys

pdbr = sys.argv[1]
naccess_file = sys.argv[2]
cutoff = float(sys.argv[3])
mode = sys.argv[4] #abs or rel

"""
Computes surface accessibility using NACCESS
Integer residue
 *Float absolute
 *Float relative
 *Float absolute_sidechain
 *Float relative_sidechain
 *Float absolute_mainchain
 *Float relative_mainchain
ATOM     14  C   ILE A   3      -4.504   0.597 -17.607   99   0.000 0 1.00
"""
ll = [ l.split() for l in open(naccess_file).readlines()]
if mode == "rel":
    naccess = [ [float(l[4]), float(l[6])] for l in ll]
elif mode == 'abs':
    naccess = [ [float(l[3]), float(l[5])] for l in ll]

nres1 = len([l for l in open (pdbr).readlines() if l[13:15].strip() == "CA"])
assert nres1 == len(naccess), ('the PDB and naccess files have different nb of residues')

dict_bb = {'C', 'N', 'O', 'CA'}

resind = -1
prev = None
beadind = -1
for l in open(pdbr).readlines():
    if not l.startswith('ATOM'):
        continue
    beadind += 1
    resname = l[17:20]
    atname = l[13:15].strip()
    resid = int(l[22:26])
    if resid != prev:
        resind += 1
        prev = resid
    nacc = naccess[resind][0]
    if atname in dict_bb:
        nacc = naccess[resind][1]
    if (int(nacc) > cutoff):
        print(beadind)
    #print('%s    %i'%(l[:59], acc))
    #print(int(acc))
