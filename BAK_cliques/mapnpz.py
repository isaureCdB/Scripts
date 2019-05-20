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
print("interaction mapped")

poses = p
interactions = []

###################
pairs = map_interactions
poses = range(len(poses))
sel1 = [ set([i[1] for i in interactions if i[0] == p ]) for p in poses]
print("sel1 computed")

def propagate(poses, sel, sel1):
    new_sel = []
    for p_set in sel:
        s = set()
        [ s.update(sel1[p]) for p in p_set ]
        new_sel.append(s)
    return new_sel

def concatenate(sel1, sel2, sel3):
    sel = [ p for p in sel1]
    [ sel[p].update(sel2[p]) for p in poses]
    [ sel[p].update(sel3[p]) for p in poses]
    return sel

sel2 = propagate(poses, sel1, sel1)
print("sel2 computed")

sel3 = propagate(poses, sel2, sel1)
print("sel3 computed")

sel1_bwd = [ set([i[0] for i in interactions if i[1] == p ]) for p in poses]
print("sel1_bwd computed")
sel2_bwd = propagate(poses, sel1_bwd, sel1_bwd)
print("sel2_bwd computed")
sel3_bwd = propagate(poses, sel2_bwd, sel1_bwd)
print("sel3_bwd computed")

sel = concatenate(sel1, sel2, sel3)
print("sel computed")

sel_bwd = concatenate(sel1_bwd, sel2_bwd, sel3_bwd)
print("sel_bwd computed")

sel_tot = [p for p in sel]
[ sel_tot[p].update(sel_bwd[p]) for p in poses ]
print("sel_tot computed")

#f = open("poses.list", "w")
#for p in poses:
#    print(p+1, file=f)
#f.close()

#name = npz_file.split(".npz")[0]
#f = open(name+".connected123")
#for s in sel_tot:
#    for p in sel:
#        print()
