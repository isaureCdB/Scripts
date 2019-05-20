#!/usr/bin/env python3

import numpy as np
import sys, threading
import json

'''
input: x-2frag.npz  Nb_poses spacing
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
        all_sets[p] = s  #### CHANGE p-1 to p (2-02-2018)
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
        all_sets[p] = s  #### CHANGE p-1 to p (2-02-2018)
    return all_sets

def propagate(sel, sets):
    # sel and sel1 must contain one set per pose
    new_sel = []
    for p_set in sel:
        s = set()
        [ s.update(sets[p]) for p in p_set ]
        new_sel.append(s)
    return new_sel

def propagate_all(sets):
    sels = [ [s] for s in sets]
    for f in range(nfrags-1): # fragment
        for s in range(min(nfrags-f-2, spacing-1)): #spacing
            print(f,s)
            sels[f].append(propagate(sels[f][s], sets[f+s+1]))
    sels_frags = [concatenate(s) for s in sels ]
    sels_all = concatenate(sels_frags)
    return sels_all

def concatenate(sels):
    for s in sels[1:]:
        assert len(s) == len(sels[0])
    sel = [ p for p in sels[0]]
    for s in sels[1:]:
        [ sel[p].update(s[p]) for p in range(len(sel)) ]
    return sel

npz_file = sys.argv[1]
nposes = int(sys.argv[2])
spacing = int(sys.argv[3])
npz = np.load(npz_file)
print("npz loaded")
print(npz.keys())
nfrags = npz["nfrags"]
interactions = [npz["interactions-%i"%i] for i in range(nfrags-1) ]

#propagate forward
sets_fwd = [interactions2sets(i, nposes) for i in interactions]
sels_fwd = propagate_all(sets_fwd)
print("sel_fwd computed")

#propagate backward
sets_bwd = [interactions2sets_bwd(i, nposes) for i in interactions]
sets_bwd.reverse()
sels_bwd = propagate_all(sets_bwd)
print("sel_bwd computed")

##########################
[sels_fwd[p].update(sels_bwd[p]) for p in range(nposes)]

for cnr, c in enumerate(sels_fwd):
    for i in c:
       assert cnr in sels_fwd[i], (cnr, i)

sels_bwd = []
print("sel_tot computed")
mapping = {}
i=0
for p in range(nposes):
    if len(sels_fwd[p]):
        mapping[p] = i
        i+=1

sels_tot = []
for p in range(nposes):
    sel = sels_fwd[p]
    if not len(sel): continue
    sels_tot.append([mapping[pp] for pp in sel])

for cnr, c in enumerate(sels_tot):
    for i in c:
       assert cnr in sels_tot[i], (cnr, i)

name = npz_file.split(".npz")[0]
f = open(name + "_connected-spacing%i.list"%spacing, "w")
mm = list(mapping.keys())
mm.sort()
for p in mm:
    print(p+1, file=f)
f.close()
print(name + "connected printed")

sels_dict = {}
for n, s in enumerate(sels_tot):
    sels_dict[str(n)] = s
print("sel_dict created")

name = sys.argv[1].split(".npz")[0]
np.savez("%s_connected-spacing%i.npz"%(name,spacing), **sels_dict)
print("npz written")
