#!/usr/bin/env python3

import numpy as np
import sys
from rmsdlib import multifit

def tri2di(a, b, c, dinucl_mapping, dinucl_coor_count):
    f = open("trilib/"+a+b+c+"/chains-nucl.txt","r")
    mapping = [ [int(i) for i in l.split()] for l in f.readlines()]
    f.close()
    mapping_npy = np.array(mapping)
    nstruc = mapping_npy.shape[0]
    nat_a, nat_b = natoms[a], natoms[b]
    c1, c2 = dinucl_coor_count[a+b], dinucl_coor_count[b+c]
    d1, d2 = c1 + nstruc, c2 + nstruc
    dinucl_coor_count[a+b] = d1
    dinucl_coor_count[b+c] = d2
    print((a+b+c))
    d = dinucl_mapping[a+b]
    dinucl_mapping[a+b][c1:d1] = mapping_npy
    dinucl_mapping[a+b][c2:d2] = mapping_npy
    return dinucl_mapping

natoms = {}
for a in "U" "G":
    natoms[a] = int(np.load("trilib/"+a+a+a+"/conf-aa.npy").shape[1]/3)

dinucl_mapping = {}
dinucl_coor_count = {}
for a in "U" "G":
    for b in "U" "G":
        dinucl_mapping[a+b] = np.zeros((200000,2))
        dinucl_coor_count[a+b] = 0

for a in "U" "G":
    for b in "U" "G":
        for c in "U" "G":
            tri2di(a,b,c, dinucl_mapping, dinucl_coor_count)

#for k in list(dinucl_coor.keys()):
for k in list(dinucl_mapping.keys()):
    print("deredundant %s"%k, file=sys.stderr)
    mapped = np.unique(dinucl_mapping[k], axis=0)
    f = open("dilib/%s/chain-nucl.txt"%k,"w")
    for i in mapped:
        print("%i %i"%(i[0], i[1]), file=f)
    f.close()
