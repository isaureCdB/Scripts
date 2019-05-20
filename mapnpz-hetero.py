#!/usr/bin/env python3

import numpy as np
import sys, threading
from npy import *

'''
extract [list of poses] and [npz of mapped pairs] from x_yfrag.npz (homopolymer)
pairs2_npz = pairs of poses at n - n+2 in at least one chain
e.g. to use for ATTRACT clustering, then cliques computation
'''

def propagate(sel1, sel2):
    new_sel = []
    for p_set in sel1:
        s = set()
        [ s.update(sel2[p-1]) for p in p_set ]
        new_sel.append(s)
    return new_sel

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
    data, poses, sets = [], [], []
    return all_sets

npz_file = sys.argv[1]
nposes = int(sys.argv[2])
npz = np.load(npz_file)
print("npz loaded")
nfrags = npz["nfrags"]

sel1_fwd = []
sel1_bwd = []
for i in range(nfrags-1):
    print(i)
    interactions = npz['interactions-%i'%i]
    #sel1.append( [ set([i[1] for i in interactions if i[0] == p ]) for p in poses] )
    all_sets = interactions2sets(interactions, nposes)
    all_sets_bwd = interactions2sets_bwd(interactions, nposes)
    interactions = []
    sel1_fwd.append(all_sets)
    sel1_bwd.append(all_sets_bwd)
    all_sets, all_sets_bwd = [], []

npz, interactions = [], []

sel_fwd = [ set() for p in range(nposes)]
for frag in range(nfrags-1):
    sel1 = [ set([p+1]) for p in range(nposes)]
    for i in range(1, min(4, nfrags-frag)):
        sel2 = sel1_fwd[frag+i-1]
        new_sel = propagate(sel1, sel2)
        sel1 = new_sel
        [ sel_fwd[p].update(new_sel[p]) for p in range(nposes) ]
        print("sel_fwd %i %i computed"%(frag, frag+i))
    sel1_fwd[frag] = []

sel1_fwd = []
print("sel_fwd computed")
##########################
#sel_bwd = [ [i+1 for i in range(nposes) if p+1 in sel_fwd[i] ] for p in range(nposes) ]
print(len(sel1_bwd))
sel_bwd = [ set() for p in range(nposes)]
for frag in range(nfrags, 1, -1):
    sel1 = [ set([p+1]) for p in range(nposes)]
    for i in range(1, min(4, frag)):
        sel2 = sel1_bwd[frag-i-1]
        new_sel = propagate(sel1, sel2)
        sel1 = new_sel
        [ sel_bwd[p].update(new_sel[p]) for p in range(nposes) ]
        print("sel_bwd %i %i computed"%(frag, frag-i))
    sel1_bwd[frag-2] = []

sel1_bwd = []
print("sel_bwd computed")
##########################3
sel_tot = sel_fwd
[ sel_tot[p].update(sel_bwd[p]) for p in range(nposes) ]
print("sel_tot computed")
sel_bwd = []

sel_dict = {}
for p in range(nposes):
    sel_dict[str(p+1)] = list(sel_tot[p])

name = sys.argv[1].split(".npz")[0]
np.savez(name + "-connected123.npz", **sel_dict)
print("connected123 written")

name = npz_file.split(".npz")[0]
f = open(name + ".connected-2", "w")
for p in range(nposes):
    if len(sel_tot[p]) > 0:
        print(p+1, file=f)
f.close()
print(name + "connected printed")
