#!/usr/bin/env python

import sys
import json
import numpy as np

def map_json(json_file):
    j = json.load(open(json_file))
    max_rmsd = j['max_rmsd']
    nfrags = j['nfrags']
    interactions = j['interactions']
    clusters = j['clusters']
    poses = [[ int(i['ranks'][0])-1 for i in cluster] for cluster in clusters]
    mapped_interactions = [[[poses[i][j[0]], poses[i+1][j[1]]] for j in interactions[i]] for i in range(len(interactions))]
    j=[]
    return mapped_interactions, nfrags, max_rmsd

if __name__ == "__main__" :
    interactions, nfrags, max_rmsd = map_json(sys.argv[1])
    a = {'nfrags' : nfrags, 'max_rmsd': max_rmsd }
    for i in range(nfrags-1):
        a['interactions-%i'%i] = interactions[i]
    print(a.keys())
    outp = sys.argv[1].split(".json")[0] + ".npz"
    if len(sys.argv) == 3:
        outp = sys.argv[2]
    np.savez(outp, **a)
