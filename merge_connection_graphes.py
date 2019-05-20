#!/usr/bin/env python3

import numpy as np
import sys

'''
merge frag1-2_2frag_2A.npz and frag2-5_4frag_2A.npz => frag1-5_5frag_2A.npz
'''

print("bugged", file=sys.stderr)
sys.exit()

def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    max_rmsd = npz['max_rmsd']
    interactions = []
    poses = []
    for n in range(nfrags-1):
        inter = npz["interactions-%d"%n]
        interactions.append(inter)
        print(len(inter), file=sys.stderr)
        poses.append(np.unique(inter[:,0]))
    poses.append(np.unique(inter[:,1]))
    maxp = max([max(i) for i in poses])
    return interactions, poses, maxp, nfrags, max_rmsd

def propagate(connections, poses_to_keep, maxp, direction):
    if isinstance(poses_to_keep, (list, set)):
        poses_to_keep = np.array(poses_to_keep, int)
    poses_to_keep_mask = np.zeros(maxp, dtype=bool)
    poses_to_keep_mask[poses_to_keep] = 1
    con = connections[:,0]
    if direction == "bwd":
        con = connections[:,1]
    print(poses_to_keep_mask)
    print(maxp, poses_to_keep_mask.shape)
    tokeep = np.take(poses_to_keep_mask,con)
#    print("STOP"); raise Exception
    new_poses = np.unique(connections[tokeep][:,1])
    if direction == "bwd":
        new_poses = np.unique(connections[tokeep][:,0])
    return connections[tokeep], new_poses

def combine_graphs(file1, file2):
    connection_graph1, poses_graph1, maxp_graph1, nfrags1, max_rmsd1 = map_npz(file1)
    connection_graph2, poses_graph2, maxp_graph2, nfrags2, max_rmsd2 = map_npz(file2)
    assert max_rmsd2 == max_rmsd1, "max_rmsd1 != max_rmsd2"
    n_graph1 = len(connection_graph1)
    n_graph2 = len(connection_graph2)
    x = set(poses_graph1[-1])
    poses_to_keep = np.array([p for p in poses_graph2[0] if p in x])

    poses_graph1[-1] = poses_to_keep
    for i in range(1, n_graph1+1):
        connection_graph1[-i], poses_graph1[-i-1] = propagate(np.array(connection_graph1[-i]), poses_graph1[-i], maxp_graph1, "bwd")

    poses_graph2[0] = poses_to_keep
    for i in range(n_graph2):
        connection_graph2[i], poses_graph2[i+1] = propagate(np.array(connection_graph2[-i]), poses_graph2[i], maxp_graph2, "fwd")

    np_connection_graph = connection_graph1 + connection_graph2

    merged_graph = {'nfrags': nfrags1 + nfrags2 -1, "max_rmsd": max_rmsd1}
    for ni, i in enumerate(np_connection_graph):
        merged_graph['interactions-%i'%ni] = i
    return merged_graph

if __name__ == "__main__" :
    result = combine_graphs(sys.argv[1], sys.argv[2])
    np.savez(sys.argv[3],**result)
    #connection_graph1, poses_graph1, maxp_graph1
