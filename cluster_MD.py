#!/usr/bin/env python3

'''
Cluster the frames of an ensemble of MD trajectories.

usage:  ./cluster_MD.py trajectories.list  clustering_cutoff

_ trajectories.list: test file containing the list of trajectories in .netcdf
_ clustering_cutoff: in angstrom


!!! all trajectories must have the same number of coordinates!!!
If comparing WT and mutant, select only the C-alpha.
You can also select only the binding pocket.
For those options, create a new .netcdf with ptraj, using an atom mask
'''

import numpy as np, sys, scipy, argparse
from scipy.io import netcdf

def multifit(array_atoms1, atoms2):
  """
  Fits an array of atom sets (array_atoms1) onto an atom set (atoms2)
  """
  import numpy
  assert isinstance(array_atoms1, numpy.ndarray)
  assert isinstance(atoms2, numpy.ndarray)

  assert len(array_atoms1.shape) == 3
  assert len(atoms2.shape) == 2

  assert len(atoms2) > 0
  assert array_atoms1.shape[2] == atoms2.shape[1] == 3
  assert len(atoms2) == array_atoms1.shape[1]
  L = len(atoms2)

  # must alway center the two proteins to avoid
  # affine transformations.  Center the two proteins
  # to their selections.
  COM1 = numpy.sum(array_atoms1,axis=1) / float(L)
  COM2 = numpy.sum(atoms2,axis=0) / float(L)

  array_atoms1 = array_atoms1 - COM1[:,numpy.newaxis, :]
  atoms2 = atoms2 - COM2

  # Initial residual, see Kabsch.
  E0 = numpy.sum( numpy.sum(array_atoms1 * array_atoms1,axis=1),axis=1) + numpy.sum( numpy.sum(atoms2 * atoms2,axis=0),axis=0)

  #
  # This beautiful step provides the answer.  V and Wt are the orthonormal
  # bases that when multiplied by each other give us the rotation matrix, U.
  # S, (Sigma, from SVD) provides us with the error!  Isn't SVD great!
  d = numpy.einsum("ijk,jl->ikl", array_atoms1, atoms2)
  V, S, Wt = numpy.linalg.svd( d )

  # We already have our solution, in the results from SVD.
  # we just need to check for reflections and then produce
  # the rotation.  V and Wt are orthonormal, so their det's
  # are +/-1.0 (and thus products are +/- 1.0 ).
  reflect = numpy.linalg.det(V) * numpy.linalg.det(Wt)

  S[:,-1] *= reflect
  V[:,:,-1] *= reflect[:, numpy.newaxis]
  U = numpy.einsum('...ij,...jk->...ki', V, Wt)
  RMSD = E0 - (2.0 * S.sum(axis=1))
  RMSD = numpy.sqrt(abs(RMSD / L))
  return U, COM1-COM2, RMSD

def fit_multi_npy(a, ref):
    rotation, translation, RMSD = multifit(a, ref)
    rot = np.transpose(rotation, axes=(0,2,1))
    COM = a.sum(axis=1)/a.shape[1]
    centered = a - COM[:,None,:]
    rotated = np.einsum('...ij,...jk->...ik',centered,rot)
    fitted = rotated + COM[:,None,:]
    translated = fitted - translation[:,None,:]
    return translated, RMSD

def cluster(structures, threshold, already_clustered, chunksize):
    """Clusters structures using an RMSD threshold
    First structure becomes a cluster,
     second structure only if it doesn't cluster with the first, etc.

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
    #  assign all structures to the closest cluster center
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

    return clusters, clustids

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('list')
parser.add_argument('threshold')
parser.add_argument("--fit",help="fit on first structure", action="store_true")
parser.add_argument("--maxframe",help="maximal total number of frames", type=int)
args = parser.parse_args()
#######################

mdfilelist = args.list
threshold = float(args.threshold)

maxframe = 1000000
if args.maxframe is not None:
    maxframe = args.maxframe

print("*************  %s *************"%mdfilelist)
frametot = 0
bornes = [0]
for nl, l in enumerate(open(mdfilelist).readlines()):
    print(l)
    ll = l.split()
    mdfile = ll[0]
    a = scipy.io.netcdf.netcdf_file(mdfile, mmap=False)
    coor = a.variables['coordinates']
    nat = coor.shape[1]
    #print(coor.shape, file = sys.stderr)
    dirname = ll[0].split('/run')[0]
    if nl == 0:
        coortot = np.zeros((maxframe, nat, 3))
    nframe = coor.shape[0]
    coortot[frametot: frametot + nframe] = coor[:nframe]
    frametot += nframe
    bornes.append(frametot)
    if frametot > maxframe:
        raise NameError('too many frames')

fitted = coortot[:frametot]
if args.fit:
    fitted, rmsd = fit_multi_npy(fitted, fitted[0])
    print(max(rmsd))

chunksize = 1000
if frametot <  chunksize:
    chunksize = frametot

clustlist = open(mdfilelist+"-clust"+str(threshold), "w")
clustnpy = open(mdfilelist+"-clust"+str(threshold)+".npy", "w")
clustmap = open(mdfilelist+"-clust"+str(threshold)+".mapping", "w")
clustpopu = open(mdfilelist+"-clust"+str(threshold)+".population", "w")

c, clustids = cluster(fitted, threshold, 0, chunksize)

csort = sorted(c, key=lambda k: len(c[k]), reverse=True)
npclust = fitted[csort]
#intervales = {b:set() for b in bornes}
for nk, k in enumerate(csort):
    # !!! changed to start at 1 !!! 18/12/17
    print("cluster %i => "%(nk+1), end='', file=clustlist),
    popu = set()
    for j in c[k]:
        print("%i "%(j+1), end=' ', file = clustlist)
        print("%i %i"%(j+1, nk+1),file = clustmap)
        for i in range(len(bornes)):
            if j > bornes[i] and j <  bornes[i+1]:
                popu.add(i)
    for p in popu:
        print("%i %i"%(nk+1, p+1), file = clustpopu)
    #print(" ".join(list(popu)), file = clustpopu)
    print('', file = clustlist)

clustmap.close()
clustlist.close()
clustpopu.close()
#np.save(clustnpy, npclust)
#clustlist.close()
