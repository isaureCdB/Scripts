#!/usr/bin/env python3

import numpy as np
import sys
from rmsdlib import multifit
from scipy.spatial.distance import squareform, pdist

def fastcluster(structures, threshold, already_clustered = 0, chunksize = 1000):
    """Clusters structures using an RMSD threshold
    First structure is kept,
     second structure is kept only if it doesn't cluster with the first, etc.
    structures: 2D numpy array, second dimension = 3 * natoms
      structures must already have been fitted!
    threshold: RMSD threshold (A)
    already_clustered: if nonzero, the first already_clustered structures are
     considered clusters
    chunksize: number of structures to put in a chunk
      This is an implementation detail that only affects the speed, not the result
    """
    if len(structures.shape) == 3:
        assert structures.shape[2] == 3
        structures = structures.reshape(structures.shape[0], structures.shape[1]*3)
    if len(structures.shape) == 2:
        assert structures.shape[1] % 3 == 0
    natoms = structures.shape[1]/3
    # threshold2 = sum-of-sd threshold = (RMSD threshold **2) * natoms
    threshold2 = threshold**2 * natoms
    nclus = 1
    assert already_clustered >= 0
    if already_clustered == 0:
        already_clustered = 1 ## the first structure is always a cluster
    clus_space = 99 + already_clustered
    clus = np.zeros((clus_space, structures.shape[1]))
    clus[:already_clustered] = structures[:already_clustered]
    clustids = list(range(already_clustered))
    for n in range(already_clustered, len(structures), chunksize):
        chunk = structures[n:n+chunksize]
        d = chunk[:, np.newaxis, :] - clus[np.newaxis, :, :]
        inter_sd = np.einsum("...ij,...ij->...i", d, d)
        #close_inter is a 2D Boolean matrix:
        #  True  (1): chunk[i] is close to (within RMSD threshold of) clus[j]
        #  False (0): chunk[i] is not close to clus[j]
        close_inter = (inter_sd < threshold2)
        # newclustered contains all structures in the chunk that *don't* cluster with an existing cluster
        newclustered = []
        for chunk_index, closest_inter in enumerate(np.argmax(close_inter,axis=1)):
            # closest_inter contains the *first* index of close_inter
            #   with the highest value of close_inter
            # We are interested in the case where close_inter is all False (=> new cluster)
            # In that case, the highest value of close_inter is False, and closest_inter is 0
            # If close_inter is *not* all False (=> existing cluster), one of these conditions is False
            if closest_inter == 0 and close_inter[chunk_index, 0] == False:
                newclustered.append(chunk_index)
        if len(newclustered):
            # Now we have newclustered: the *chunk* index of all structures in the chunk that will be in new clusters
            # Now we want to cluster them among themselves, and add the *structure* id of each new cluster
            chunk_newclustered = chunk[newclustered]
            d = chunk_newclustered[:, np.newaxis, :] - chunk_newclustered[np.newaxis, :, :]
            intra_sd = np.einsum("...ij,...ij->...i", d, d)
            close_intra = (intra_sd < threshold2)

            # set all upper-triangular indices to False
            close_intra[np.triu_indices(len(chunk_newclustered))] = 0
            for nn in range(len(chunk_newclustered)):
                # same logic as for closest_inter;
                #  except that we don't have the chunk index, but the chunk_newclustered index (nn)
                #  and, since we modify close_intra in the "else" clause, argmax is computed later
                closest_intra = np.argmax(close_intra[nn])
                if closest_intra == 0 and close_intra[nn, 0] == False:
                    chunk_index = newclustered[nn]
                    # if clus is full, re-allocate it as a 50 % larger array
                    if nclus == clus_space:
                        clus_space = int(clus_space*1.5)
                        clus_old = clus
                        clus = np.zeros((clus_space, structures.shape[1]))
                        clus[:nclus] = clus_old
                    clus[nclus] = chunk[chunk_index]
                    clustids.append(n+chunk_index)
                    nclus += 1
                else:  # in addition, if we aren't a new cluster, being close to us doesn't matter
                    close_intra[:, nn] = False
    # After assigning the cluster centers,
    #  assign all structures to the closest cluster
    clusters = {a:[a] for a in clustids}
    for n in range(0, len(structures), chunksize):
        chunk = structures[n:n+chunksize]
        d = chunk[:, np.newaxis, :] - clus[np.newaxis, :, :]
        inter_sd = np.einsum("...ij,...ij->...i", d,d)
        best = np.argmin(inter_sd, axis=1)
        for nn in range(len(chunk)):
            bestclust = clustids[best[nn]]
            if bestclust == (n+nn):
                continue
            clusters[bestclust].append(n+nn)
    clust = list(clusters.values())
    return clust, clustids

def fit_multi_npy(a):
    ref = a[0] ###########################################
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a.sum(axis=1)/a.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

def deredundant(structures, seq, threshold, chunksize=1000):
    clustlist = open("dilib/"+seq+"-aa-clust"+str(threshold), "w")
    clustnpy = "dilib/"+seq+"-aa-clust"+str(threshold)+".npy"
    c, _ = fastcluster(structures, threshold,chunksize )
    csort = sorted(c, key=lambda cc: len(cc), reverse=True)
    first = [ c[0] for c in csort]
    npclust = structures[first]
    for nk, k in enumerate(csort):
        print("cluster %i => "% (nk+1), end=' ', file=clustlist)
        for j in k:
            print("%i "%(j+1), end=' ', file=clustlist)
        print(file=clustlist)
    np.save(clustnpy, npclust)
    clustlist.close()

def tri2di(a, b, c, dinucl_coor, dinucl_coor_count, dinucl_mapping ):
    trinucl = np.load("trilib/"+a+b+c+"-aa.npy")
    #f = open("trilib/"+a+b+c+"/chains-nucl.txt")
    #mapping = [ [int(i) for i in l.split()] for l in open(f).readlines()]
    #f.close()
    #mapping_npy = np.array(mapping)
    nstruc = trinucl.shape[0]
    nat_a, nat_b = natoms[a], natoms[b]
    dinucl_1 = trinucl[:,:(nat_a + nat_b),:]
    dinucl_2 = trinucl[:,nat_a:,:]
    c1, c2 = dinucl_coor_count[a+b], dinucl_coor_count[b+c]
    d1, d2 = c1 + nstruc, c2 + nstruc
    print((a+b+c))
    dinucl_coor[a+b][c1:d1] = dinucl_1
    dinucl_coor[b+c][c2:d2] = dinucl_2
    dinucl_coor_count[a+b] = d1
    dinucl_coor_count[b+c] = d2
    #dinucl_mapping[a+b][c1:d1] = mapping_npy
    #dinucl_mapping[a+b][c2:d2] = mapping_npy
    return dinucl_coor, dinucl_coor_count, dinucl_mapping

def read_clustfile(clustfile):
  clust = []
  for l in open(clustfile):
    ll = l.split()[3:]
    clust.append([int(v) for v in ll])
  return clust

def subclust(coors, rootclusters, cutoff ):
    #rootclusters = read_clustfile(clustfile)
    superclust, subclust = [], []
    maxstruc = 10000
    coorsize, natom = coors.shape[:2]
    assert coorsize < 10000, "too many structures in subcluster"
    print(coors.shape)
    lim = cutoff * cutoff * natom
    clust_struc = np.zeros(dtype=float,shape=(coorsize, natom*3))
    struc_counter = 0
    for rootclustnr, rootclust in enumerate(rootclusters):
        if len(rootclust) == 1:
          subclust.append(rootclust)
          superclust.append([len(subclust)])
          struc_counter += 1
          continue
        leafclust = []
        for cnr, c in enumerate(rootclust):
            if cnr == 0 and rootclustnr == 0: continue
            struc_counter += 1
            coor = coors[struc_counter]
            clust_struc[cnr] = coor.reshape(natom*3)
        d = squareform(pdist(clust_struc[:len(rootclust)], 'sqeuclidean'))
        d2 = d<lim
        clustered = 0
        while clustered < len(rootclust):
          neigh = d2.sum(axis=0)
          heart = neigh.argmax()
          leaf = np.where(d2[heart])[0]
          for cs in leaf:
            d2[cs,:] = False
            d2[:, cs] = False
          leaf = [heart+1] + [v+1 for v in leaf if v != heart]
          leafclust.append(leaf)
          clustered += len(leaf)
        #
        mapped_root = []
        for leaf in leafclust:
          mapped_leaf = [rootclust[n-1] for n in leaf]
          subclust.append(mapped_leaf)
          mapped_root.append(len(subclust))
        superclust.append(mapped_root)
    return superclust, subclust

cutoff = float(sys.argv[1])
chunksize = int(sys.argv[2])
na = sys.argv[3]

bases = ["U", "G"]
if na == 'dna':
    bases = ["T", "G"]

natoms = {}
for a in bases:
    natoms[a] = int(np.load("trilib/"+a+a+a+"-aa.npy").shape[1]/3)

dinucl_coor = {}
dinucl_coor_count = {}
dinucl_mapping = {}
for a in bases:
    for b in bases:
        dinucl_coor[a+b] = np.zeros((200000,natoms[a]+natoms[b],3))
        dinucl_mapping = np.zeros((200000,2))
        dinucl_coor_count[a+b] = 0

for a in bases:
    for b in bases:
        for c in bases:
            tri2di(a,b,c, dinucl_coor, dinucl_coor_count, None)

for k in list(dinucl_coor.keys()):
    dinucl_coor[k] = dinucl_coor[k][:dinucl_coor_count[k]]
    print((k, dinucl_coor[k].shape))

for k in list(dinucl_coor.keys()):
    print("deredundant %s"%k, file=sys.stderr)
    #template = np.load("dilib/"+k+"/template.npy")
    #        template = template.reshape((1,template.shape[0],3))
    # each dinucl is present twice. ex:GU from U[GU] and from [GU]U
    # only terminal dinucl in chain are present once.
    dinucl = np.unique(dinucl_coor[k], axis=0)
    #map = np.unique(dinucl_mapping[k], axis=0)
    ###dinucl_fitted, RMSD = fit_multi_npy(dinucl, template)
    dinucl_fitted, RMSD = fit_multi_npy(dinucl)
    ###rootclusters, clustids = fastcluster(dinucl_fitted, 3*cutoff)
    ###print("%i subclusters"%len(rootclusters), file=sys.stderr)
    ###superclust, subclust = subclust(dinucl_fitted, rootclusters, cutoff)
    deredundant(dinucl_fitted, k, cutoff, chunksize)
