#!/usr/bin/env python3

import sys
import numpy as np
import scipy.spatial

def pdb2npy(p):
    ll = [l for l in open(p).readlines() if l.startswith("ATOM")]
    coor = [ [float(i) for i in [l[30:38], l[38:46], l[46:54]]] for l in ll ]
    return np.array(coor)

#com = pdb2npy(sys.argv[1])
com=np.load(sys.argv[1])
#com = np.array([ [float(i) for i in l.split()] for l in open(sys.argv[1]).readlines()])
grid = pdb2npy(sys.argv[2])
cutoff = float(sys.argv[3])

#print(grid.shape, file=sys.stderr)
Y = scipy.spatial.cKDTree(grid)
for c in com:
    distances, indices = Y.query(c, k=+99999, distance_upper_bound = cutoff)
    nr_neighbors = (distances<np.inf).sum()
    print(nr_neighbors, file=sys.stderr)
    indices = indices[:nr_neighbors]
    #if isinstance(neighbor[0], np.ndarray):
    for i in indices:
        print(i+1, end=" "),
    print('')
#np.save(outp, nlist)
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/closest_grid_point.py
