#!/usr/bin/env python3

import sys
import numpy as np
from scipy.spatial.distance import pdist, squareform
from math import sqrt

npy_file = sys.argv[1]
cutoff = float(sys.argv[2])
output_clust = npy_file.split(".npy")[0]+"-clust"+str(cutoff)
output_npy = npy_file.split(".npy")[0]+"-clust"+str(cutoff) + ".npy"


def write_clustfile(clust, clustfile):
  cf = open(clustfile, "w")
  for cnr, c in enumerate(clust):
    print("Cluster %d ->" % (cnr+1), end=' ', file=cf)
    for cc in c: print(cc, end=' ', file=cf)
    print("", file=cf)

clust = []
maxstruc = 100000

coors = np.load(npy_file)
nstruc, natoms = coors.shape[:2]
lim = cutoff * cutoff * natoms
clust_struc = np.zeros(dtype=float,shape=(maxstruc,natoms,3))
clust_struc[:nstruc] = coors
nfloat = natoms*3

struc_counter = 0

d = squareform(pdist(clust_struc[:nstruc].reshape(nstruc, nfloat), 'sqeuclidean'))
d2 = d<lim
clustered = 0
while clustered < nstruc:
  neigh = d2.sum(axis=0)
  heart = neigh.argmax()
  leaf = np.where(d2[heart])[0]
  for cs in leaf:
    d2[cs,:] = False
    d2[:, cs] = False
  leaf = [heart+1] + [v+1 for v in leaf if v != heart]
  clust.append(leaf)
  clustered += len(leaf)

write_clustfile(clust, output_clust)
clust_npy = coors[[c[0]-1 for c in clust]]
np.save(output_npy, clust_npy)
