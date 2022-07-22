#!/usr/bin/env python3

import numpy as np
import sys
from rmsdlib import multifit


def tri2di(npy, d_coor, d_coor_count, d_mapping):
    trinucl = np.load(npy)
    nstruc = trinucl.shape[0]
    nat = trinucl.shape[1]
    dinucl_1 = trinucl[:,:2*nat,:]
    dinucl_2 = trinucl[:,nat+1:,:]
    c1, c2 = d_coor_count[a+b], d_coor_count[b+c]
    d1, d2 = c1 + nstruc, c2 + nstruc
    print((a+b+c))
    d_coor[a+b][c1:d1] = dinucl_1
    d_coor[b+c][c2:d2] = dinucl_2
    d_coor_count[a+b] = d1
    d_coor_count[b+c] = d2
    d_mapping[a+b][c1:d1] = mapping_npy
    d_mapping[a+b][c2:d2] = mapping_npy
    return d_coor, d_coor_count, d_mapping

def fit_multi_npy(a, ref):
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a.sum(axis=1)/a.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

natoms = {}
for a in "U" "G":
    natoms[a] = int(np.load("trilib/"+a+a+a+"/conf-aa.npy").shape[1]/3)

d_coor = {}
d_coor_count = {}
d_mapping = {}
for a in "U" "G":
    for b in "U" "G":
        d_coor[a+b] = np.zeros((200000,natoms[a]+natoms[b],3))
        d_coor_count[a+b] = 0
        d_mapping[a+b] =  np.zeros((200000, 2))

d_coor, d_coor_count, d_mapping = tri2di(d_coor, d_coor_count, d_mapping)

for k in list(d_coor.keys()):
    d_coor[k] = d_coor[k][:d_coor_count[k]]
    d_mapping[k] = d_mapping[k][:d_coor_count[k]]
    print("%i dinucl for sequence %s"%(len(d_coor[k]), k))

#for k in list(d_coor.keys()):
for k in list(d_coor.keys()):
    template = np.load("dilib/"+k+"/template.npy")
    #        template = template.reshape((1,template.shape[0],3))
    dinucl, u1 = np.unique(d_coor[k], axis=0, return_index=True)
    dinucl_fitted, RMSD = fit_multi_npy(dinucl, template)
    dinucl_uniq, u2 = np.unique(dinucl_fitted, axis=0, return_index=True)
    print("%i dr=> %i fit-dr=> %i dinucl %s"%(len(d_coor[k]), len(u1), len(u2), k))
    mapping = d_mapping[k][u1][u2]
    np.save("dilib/"+k+"/conf-aa-all.npy",dinucl_uniq)
    f = open("dilib/"+k+"/conf-aa-all.chains-nucl", "w")
    for i in mapping:
        print("%i %i"%(i[0], i[1]), file=f)
    f.close()
