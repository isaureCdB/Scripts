#!/usr/bin/env python3
import numpy as np
import sys

def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    max_rmsd = 'max_rmsd'
    clusters, inter =  [], []
    if 'interactions-0' in npz.keys():
        for n in range(nfrags-1):
            inter.append(npz["interactions-%i"%n])
        for n in range(nfrags):
            clusters.append(npz["clusters-%i"%n])
    else:
        for n in range(nfrags-1):
            inter.append(npz["interactions-%i"%(n+1)])
        for n in range(nfrags):
            clusters.append(npz["clusters-%i"%(n+1)])
    npz = []
    p = [[ int(i)-1 for i in cluster] for cluster in clusters]
    interactions = [ np.array([[p[i][j[0]], p[i+1][j[1]]] for j in inter[i]], dtype=int) for i in range(len(inter))]
    return interactions, nfrags, max_rmsd

if __name__ == "__main__" :
    interactions, nfrags, max_rmsd = map_npz(sys.argv[1])
    a = {'max_rmsd': max_rmsd, 'nfrags' : nfrags}
    for i in range(nfrags-1):
        a['interactions-%i'%i] = interactions[i]
    print(a.keys())
    np.savez(sys.argv[2], **a)
