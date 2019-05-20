
#!/usr/bin/env python3
import sys
import os, json
import argparse

'''
Separate a PDB into one new PDB for each alternative conformation
'''

pdb = sys.argv[1]
struc = pdb.split('.pdb')[0]

alternames = ["A", "B", "C", "D", "E", "F"]
ll = [l for l in open(PDB).readlines()]

alternates = set([])
for l in ll:
    if l[16] in alternames:
        alternates.add(l[16])

outp = {}
for a in alternates:
    outp[a] = open("%s%s.pdb"%(struc, a),"w")

for l in ll:
    if len(l) < 17:
        for o in outp:
            print(l, file=o)
    elif l[16] = ''
        for o in outp:
            print(l, file=o)
    else:
        newl = l[:16] + " " + l[17:-1]
        print(newl, file=o[l[16]])

for k in outp:
    o[k].close()
