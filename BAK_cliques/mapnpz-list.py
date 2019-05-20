#!/usr/bin/env python3

import numpy as np
import sys, threading
from npy import *

'''
extract [list of poses] and [npz of mapped pairs] from x_yfrag.npz (homopolymer)
pairs2_npz = pairs of poses at n - n+2 in at least one chain
e.g. to use for ATTRACT clustering, then cliques computation

TO FINISH : change np arrays into lists
'''

npz_file = sys.argv[1]
name = sys.argv[1].split(".npz")[0]
poses_list = name + ".poses_list"
pairs1_npy = name + ".pairs1"
pairs2_npy = name + ".pairs2"
pairs3_npy = name + ".pairs3"

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

poses = p
f = open("poses.list", "w")
for p in poses:
    print(p, file=f)
f.close()

###################
pairs = map_interactions
poses = range(len(poses))
sel1 = [ pairs[np.where(pairs[:,0]==p)[0], 1] for p in poses]

def propagate(poses, sel):
    new_sel = []
    for p in poses:
        s2 = set([])
        for s in sel[p]:
            w = pairs[np.where(pairs[:,0]==s)[0], 1]
            s2.update(w)
        new_sel.append(list(s2))
    return new_sel

def reverse(sel):
    rev = [ [j for j in poses if i in sel[j]] for i in poses ]
    tot = [ list(set(sel[i] + rev[i])) for i in poses ]
    return tot

sel2 = propagate(poses, sel1)
sel3 = propagate(poses, sel2)
sel123 = [ sum([sel1[i], sel2[i], sel3[i]], []) for i in poses]

#tot_sel1 = reverse(sel1)
#tot_sel2 = reverse(sel2)
#tot_sel3 = reverse(sel3)

tot_sel123 = reverse(sel123)

np.savez(poses_list, **poses)
#np.save(pairs1_npy, tot_sel1)
#np.save(pairs2_npy, tot_sel2)
#np.save(pairs3_npy, tot_sel3)

np.save(pairs123_npy, tot_sel123)
