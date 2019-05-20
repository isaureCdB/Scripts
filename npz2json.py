#!/usr/bin/env python3
import sys
import json
import numpy as np

inp, output = sys.argv[1:]
npz = np.load(inp)

nfrags = npz['nfrags']
max_rmsd = npz['max_rmsd']
cl = [ [] for n in range(nfrags) ]

new_interactions = [np.zeros(npz["interactions-%d" % n].shape,dtype=int) for n in range(nfrags-1)]
for frag in range(nfrags):
    ranks = []
    if frag > 0:
        ranks.append(npz["interactions-%d" % (frag-1)][:, 1])
    if frag < nfrags-1:
        ranks.append(npz["interactions-%d" % frag][:, 0])
    allranks = np.concatenate(ranks)
    unique, unique_indices = np.unique(allranks, return_inverse=True)
    pos = 0
    if frag > 0:
        size = len(ranks[0])
        new_interactions[frag-1][:,1] = unique_indices[:size]
        pos += size
    if frag < nfrags-1:
        new_interactions[frag][:,0] = unique_indices[pos:]
    cl[frag] = [{"ranks": [v+1], "radius": 0} for v in unique.tolist()]
new_interactions = [item.tolist() for item in new_interactions]

j = {
    "nfrags": int(nfrags),
    "max_rmsd": float(max_rmsd),
    "clusters": cl,
    "interactions": new_interactions
}
json.dump(j, open(output, "w"),sort_keys=True)
