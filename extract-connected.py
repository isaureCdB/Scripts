#!/usr/bin/env python3

import numpy as np, sys

npzfile=sys.argv[1]
n = np.load(npzfile)
f1 = int(sys.argv[2])

nfrags = n['nfrags']
interactions = [ n['interactions-%i'%i] for i in range(nfrags-1)]
for nr, i in enumerate(interactions):
    f = open(npzfile.split(".npz")[0] + ".frag%i"%(f1+nr), "w")
    poses = np.unique(i[:,0])
    for p in poses:
        print(p+1, file=f)
    f.close

f = open(npzfile.split(".npz")[0] + ".frag%i"%(f1+nfrags-1), "w")
poses = np.unique(interactions[-1][:,1])
for p in poses:
    print(p+1, file=f)
f.close
