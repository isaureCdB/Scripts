#!/usr/bin/env python3
import sys
import numpy as np
from rotmat2euler import rotmat2euler

def file2nparray(filename):
    lines = [ l for l in open(filename, "r")]
    rottrans_mat = [[]]
    for l in lines:
        if len(l)<3:
            rottrans_mat.append([])
            continue
        j = [float(i) for i in l.split()]
        rottrans_mat[-1].append(j)
    rottrans_mat = np.array(rottrans_mat)
    s = rottrans_mat.shape
    if len(s) == 2:
        rottrans_mat = rottrans_mat.reshape((1,s[0], s[1]))
    return rottrans_mat

def mat2rottrans(mat):
    trans_mat = rottrans[:,:-1,-1]
    rot_mat = rottrans[:,:-1,:-1]
    return rot_mat, trans_mat

def printmat(rot, trans):
    for i in rot:
        print(" %s"%str(i)),
    for i in trans:
        print(" %s"%str(i)),
    print("")

recmat = sys.argv[1]
ligmat = sys.argv[2]
indices_file = sys.argv[3]

rottrans_mat_rec = file2nparray(recmat)
rottrans_mat_lig = file2nparray(ligmat)

print("#pivot 1 0 0 0")
print("#pivot 2 0 0 0")
print("#centered receptor: false")
print("#centered ligands: false")
nstruc = 1

indices_lines = [ int(l.split()[0]) for l in open(indices_file, "r")]
indices = np.array(indices_lines)

nrec = len(indices)
nlig = sum(indices)
assert nrec == rottrans_mat_rec.shape[0], ( nrec, rottrans_mat_rec.shape)

count = 0
for r in range(nrec):
    rot_rec = rotmat2euler(rottrans_mat_rec[r])
    trans_rec = rottrans_mat_rec[r,:-1,-1]
    nlig = indices[r]
    for lig in rottrans_mat_lig[count:count + nlig]:
        rot_lig = rotmat2euler(lig)
        trans_lig = lig[:-1,-1]
        print("#%i"%nstruc)
        printmat(rot_rec, trans_rec)
        printmat(rot_lig, trans_lig)
        nstruc += 1
    count += nlig
