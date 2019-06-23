#!/usr/bin/env python3

'''
Usage:
 compute_overlap_frag.py frag1-preatoms.npy frag2-postatoms.npy \
 --sel1 sel1.list --sel2 sel2.list > outp.ormsd
'''
import sys, argparse, json
import numpy as np

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('frag1')
parser.add_argument('frag2')
parser.add_argument("--sel1",help="selection (indices) of coordinates from frag1")
parser.add_argument("--sel2",help="selection (indices) of coordinates from frag2")
parser.add_argument("--connections",help="json frag1-frag2 connectivity graph")
args = parser.parse_args()
#######################
def npy2to3(npy):
    if len(npy.shape) == 2:
        if npy.shape[1] == 3:
            npy = npy.reshape(1, npy.shape[0], npy.shape[1])
        else:
            npy = npy.reshape(npy.shape[0], int(npy.shape[1]/3), 3)
    else:
        assert len(npy.shape) == 3
    return npy

coor1 = npy2to3(np.load(args.frag1))
coor2 = npy2to3(np.load(args.frag2))

if sel1 is not None:
    sel1 = [int(l.split()[0]) for l in open(args.sel1).readlines()]
    coor1 = coor1[sel1]

if sel2 is not None:
    sel2 = [int(l.split()[0]) for l in open(args.sel2).readlines()]
    coor2 = coor2[sel2]

graph = json.load(open(args.connections))
indices1 = [d["ranks"][0] for d in graph['clusters'][0]]
indices2 = [d["ranks"][0] for d in graph['clusters'][1]]
connections = graph['interactions'][0]
connections = np.array(connections)
map_connections1 = indices1[connections[:,0]]
map_connections2 = indices2[connections[:,1]]

chunk = 100000
rmsd = np.zeroes(len(connections))
for s in range(0,len(connections),chunk):
    coor_connections1 = coor1[map_connections1[s:s+chunk]]
    coor_connections2 = coor2[map_connections2[s:s+chunk]]
    d = coor_connections1 - coor_connections2
    msd = np.einsum("...ijk,...ijk->...i", d,d)
    rmsd[s:s+chunk] = (msd/c1.shape[1])**0.5

#np.savetxt(sys.stdout, rmsd, fmt'%.18e')
#map_connections = [ [indices1[i], indices2[j]] for [i, j] in connections ]

for i, j, r in zip(map_connections+1, map_connections2+1, rmsd):
    print("%i %i %.2f"%(i, j, r))
