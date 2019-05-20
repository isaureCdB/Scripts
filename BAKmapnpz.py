#!/usr/bin/env python3

import numpy as np
import sys, threading
from npy import *

'''
extract [list of poses] and [npz of mapped pairs] from x_yfrag.npz (homopolymer)
pairs2_npz = pairs of poses at n - n+2 in at least one chain
e.g. to use for ATTRACT clustering, then cliques computation
'''

npz_file = sys.argv[1]
name = npz_file.split(".npz")[0]
poses_list = name + "_poses.list"
pairs1_npy = name + "_pairs1.npy"
pairs2_npy = name + "_pairs2.npy"
pairs3_npy = name + "_pairs3.npy"
pairs123_npy = name + "_pairs123.npy"

npz = np.load(npz_file)
nfrags = npz["nfrags"]
poses, interactions =  [], []
for n in range(nfrags-1):
    inter = npz["interactions-%d"%n]
    interactions.append(inter)
    poses.append(np.unique(inter[:,0]))

poses.append(np.unique(inter[:,1]))
p = np.unique(np.concatenate(poses))
pairs = np.unique(np.concatenate(interactions, axis=0), axis=0)
map_interactions = np.array([ [np.where(p==i[0])[0][0], np.where(p==i[1])[0][0]] for i in pairs ])
poses = p
interactions = []

f = open("poses.list", "w")
for p in poses:
    print(p+1, file=f)
f.close()

###################
pairs = map_interactions
poses = range(len(poses))
sel1 = np.array([ pairs[np.where(pairs[:,0]==p)[0], 1] for p in poses])
#sel2 = [ pairs[np.where(pairs[:,0]==s)[0], 1] for p in poses for s in sel1[p]]
#sel3 = [ pairs[np.where(pairs[:,0]==s)[0], 1] for p in poses for s in sel2[p]]

def propagate(poses, sel):
    new_sel = []
    for p in poses:
        s2 = []
        for s in sel[p]:
            w = pairs[np.where(pairs[:,0]==s)[0], 1]
            s2.append(w)
        if len(s2) > 0:
            new_sel.append(np.unique(np.concatenate(s2, axis=0)))
        else:
            new_sel.append([])
    return np.array(new_sel)

def reverse(sel, poses):
    rev = [ np.array([j for j in poses if i in sel[j]]) for i in poses ]
    tot = [ np.unique(np.concatenate([sel[i], rev[i]])) for i in poses]
    return tot

sel2 = propagate(poses, sel1)
sel3 = propagate(poses, sel2)
print(sel1.shape)
sel123 = np.concatenate([sel1, sel2, sel3], axis=1)
#tot_sel1 = reverse(sel1, poses)
#tot_sel2 = reverse(sel2, poses)
#tot_sel3 = reverse(sel3, poses)
tot_all = [tot_sel1, tot_sel2, tot_sel3]

sel_all = [ np.unique(np.concatenate([t[i] for t in tot_all])) for i in poses ]

#np.savez(poses_list, **poses)
np.save(pairs1_npy, tot_sel1)
np.save(pairs2_npy, tot_sel2)
np.save(pairs3_npy, tot_sel3)
np.save(pairs123_npy, sel_all)

'''
f = open(interactinons_list, "w")
for i in map_interactions:
    print("%i %i"%(i[0], i[1]), file=f)
f.close()
'''
