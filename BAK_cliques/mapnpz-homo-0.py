#!/usr/bin/env python3

import numpy as np
import sys, threading
from npy import *
import json

'''
input: x-2frag.npz  Nb_poses
outputs:
_ the list of connected poses
_ the list of pairs of poses that could connect at n+1, n+2 or n+3
e.g. to use for ATTRACT clustering, then cliques computation
'''
def interactions2sets(data, nposes):
    inds = np.argsort(data[:,0])
    data = data[inds]
    points = np.where(np.diff(data[:, 0]) != 0)[0]+1
    startpoints = np.array([0] + points.tolist())
    endpoints = np.array(points.tolist() + [len(data)])
    poses = data[startpoints,0]
    sets = [set(data[a:b,1]) for a,b in zip(startpoints, endpoints)]
    all_sets = [set() for n in range(nposes)]
    for p,s in zip(poses, sets):
        all_sets[p-1] = s
    return all_sets

def interactions2sets_bwd(data, nposes):
    inds = np.argsort(data[:,1])
    data = data[inds]
    points = np.where(np.diff(data[:,1]) != 0)[0]+1
    startpoints = np.array([0] + points.tolist())
    endpoints = np.array(points.tolist() + [len(data)])
    poses = data[startpoints,1]
    sets = [set(data[a:b,0]) for a,b in zip(startpoints, endpoints)]
    all_sets = [set() for n in range(nposes)]
    for p,s in zip(poses, sets):
        all_sets[p-1] = s
    return all_sets

def propagate(sel, sel1):
    # sel and sel1 must contain one set per pose
    new_sel = []
    for p_set in sel:
        s = set()
        [ s.update(sel1[p]) for p in p_set ]
        new_sel.append(s)
    return new_sel

def concatenate(sel1, sel2, sel3):
    assert len(sel1) == len(sel2) == len(sel3)
    sel = [ p for p in sel1]
    [ sel[p].update(sel2[p]) for p in range(len(sel))]
    [ sel[p].update(sel3[p]) for p in range(len(sel))]
    return sel

npz_file = sys.argv[1]
nposes = int(sys.argv[2])
npz = np.load(npz_file)
print("npz loaded")

interactions = npz["interactions-0"]
sel1 = interactions2sets(interactions, nposes)
#sel1= [ set([i[1] for i in interactions if i[0] == p+1 ]) for p in range(nposes)]

sel2 = propagate(sel1, sel1)
print("sel2 computed")

sel3 = propagate(sel2, sel1)
print("sel3 computed")

sel = concatenate(sel1, sel2, sel3)
print("sel computed")

sel_bwd = [ [i+1 for i in range(nposes) if p+1 in sel[i] ] for p in range(nposes) ]
print("sel_bwd computed")

sel_tot = [p for p in sel]
[ sel_tot[p].update(sel_bwd[p]) for p in range(nposes) ]
print("sel_tot computed")

sel_dict = {}
for p in range(nposes):
    sel_dict[str(p+1)] = sel_tot[p]

name = sys.argv[1].split(".npz")[0]
np.savez(name + ".connected123", **sel_dict)

name = npz_file.split(".npz")[0]
f = open(name + ".connected", "w")
for p in range(nposes):
    if len(sel_tot[p]) > 0:
        print(p+1, file=f)
f.close()
print(name + "connected printed")
