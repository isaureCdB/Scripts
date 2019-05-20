#!/usr/bin/env python3
import numpy as np
import sys, threading
from npy import *
import threading
import functools
'''
Sort poses into clashing cliques, based on atom-atom distances.
Poses that are connected at (n,n+1), (n,n+2) or (n,n+3) do not clash.
x = UUU-6frag-2A-connected
usage: python cliques-greedy-homo-npz.py x.npy UUU-6frag-2A.json 1 '5 3 1'\
       x.clust5A x.clust5A.subclust3A x.clust3A.subclust1A \
       x.clust5A.superclust3A x.clust3A.superclust1A >  UUU-6frag-2A.cliques
See cliques-homo-selection-multiproc.sh for proper usage
'''
############### from mapnpz-hetero.py #####################
# get connected poses at f+1, f+2, f+3

def propagate(sel1, sel2):
    new_sel = []
    for p_set in sel1:
        s = set()
        [ s.update(sel2[p-1]) for p in p_set ]
        new_sel.append(s)
    return new_sel

def interactions2sets(data, nposes):
    inds = np.argsort(data[:,0])
    data = data[inds]
    points = np.where(np.diff(data[:, 0]) != 0)[0]+1
    startpoints = np.array([0] + points.tolist())
    endpoints = np.array(points.tolist() + [len(data)])
    poses = data[startpoints,0]
    sets = [set(data[a:b,1]) for a,b in zip(startpoints, endpoints)]
    all_sets = [set() for n in range(nposes)]
    for p,s in zip(poses, sets):
        all_sets[p-1] = s
    return all_sets

def interactions2sets_bwd(data, nposes):
    inds = np.argsort(data[:,1])
    data = data[inds]
    points = np.where(np.diff(data[:,1]) != 0)[0]+1
    startpoints = np.array([0] + points.tolist())
    endpoints = np.array(points.tolist() + [len(data)])
    poses = data[startpoints,1]
    sets = [set(data[a:b,0]) for a,b in zip(startpoints, endpoints)]
    all_sets = [set() for n in range(nposes)]
    for p,s in zip(poses, sets):
        all_sets[p-1] = s
    data, poses, sets = [], [], []
    return all_sets

def get_sel1(npz, nposes):
    sel1_fwd = []
    sel1_bwd = []
    nfrags = npz["nfrags"]
    for i in range(nfrags-1):
        print(i)
        interactions = npz['interactions-%i'%i]
        #sel1.append( [ set([i[1] for i in interactions if i[0] == p ]) for p in poses] )
        all_sets = interactions2sets(interactions, nposes)
        all_sets_bwd = interactions2sets_bwd(interactions, nposes)
        interactions = []
        sel1_fwd.append(all_sets)
        sel1_bwd.append(all_sets_bwd)
        all_sets, all_sets_bwd, interactions = [], [], []
    return sel1_fwd, sel1_bwd

def get_connected(poses, sel1_fwd, sel1_bwd):
    # poses : list of poses i nthe pre-clique
    # TODO: map poses by selection_file !!!
    nfrags = npz["nfrags"]
    #
    sel_fwd = [ set() for p in poses]
    for frag in range(nfrags-1):
        sel1 = [ set([p+1]) for p in poses]
        for i in range(1, min(4, nfrags-frag)):
            sel2 = sel1_fwd[frag+i-1]
            new_sel = propagate(sel1, sel2)
            sel1 = new_sel
            [ sel_fwd[p].update(new_sel[p]) for p in poses ]
            print("sel_fwd %i %i computed"%(frag, frag+i))
        sel1_fwd[frag] = []
    sel1_fwd = []
    print("sel_fwd computed")
    #
    sel_bwd = [ set() for p in poses]
    for frag in range(nfrags, 1, -1):
        sel1 = [ set([p+1]) for p in poses]
        for i in range(1, min(4, frag)):
            sel2 = sel1_bwd[frag-i-1]
            new_sel = propagate(sel1, sel2)
            sel1 = new_sel
            [ sel_bwd[p].update(new_sel[p]) for p in poses ]
            print("sel_bwd %i %i computed"%(frag, frag-i))
        sel1_bwd[frag-2] = []
    sel1_bwd = []
    print("sel_bwd computed")
    ##########################3
    sel_tot = sel_fwd
    [ sel_tot[p].update(sel_bwd[p]) for p in range(nposes) ]
    print("sel_tot computed")
    sel_bwd = []
    return sel_tot

def get_clashes_p3(structures, threshold):
    import cffi
    from _get_clashes_p3 import ffi
    from _get_clashes_p3.lib import get_clashes_p3
    def npdata(a):
      return a.__array_interface__["data"][0]
    n = structures.shape[0]
    nat = structures.shape[1]
    clash_matrix = np.zeros((n, n), dtype = bool)
    ptr_structures = ffi.cast("double *", npdata(structures) )
    ptr_matrix = ffi.cast("bool *", npdata(clash_matrix) )
    get_clashes_p3(n, nat, threshold, ptr_structures, ptr_matrix)
    return clash_matrix

def sort_clashing(structures, threshold):
    n = structures.shape[0]
    tmp_cliques = []
    clash_matrix = get_clashes_p3(structures, threshold)
    clash_count = -1 * np.sum(clash_matrix, axis=0)
    order = clash_count.argsort()
    return clash_matrix, order

def checkclust(structures, sub_indices, order, connected, threshold, clash_matrix):
    tmp_cliques = []
    for nr1 in order:
        struc1  = structures[nr1]
        new_clique = True
        ''' check for each clique if struc1 can belong to it'''
        for nrcl, cl in enumerate(tmp_cliques):
            in_clique = True
            '''check for each pose in clique if struc1 clashes with it'''
            for nr2 in cl:
                ''' poses that overlap don't clash'''
                if nr1 in connected[nr2]:
                    in_clique = False
                    break
                struc2 = structures[nr2]
                ''' if poses can't clash, they can't be in same clique'''
                if clash_matrix is None:
                    struc = np.concatenate((struc1, struc2))
                    if not get_clashes_p3(struc, threshold)[0, 0]:
                        in_clique = False
                        break
                else: # we already computed the clash_matrix
                    if not clash_matrix[nr1, nr2]:
                        in_clique = False
                        break
            ''' if pose1 clashes with the whole clique, it is added to it'''
            if in_clique:
                tmp_cliques[nrcl].append(nr1)
                new_clique = False
                break
        ''' if struc1 was not added to a clique, it creates a new one'''
        if new_clique:
            tmp_cliques.append([nr1])
    map_cliques = [ [sub_indices[i] for i in cl] for cl in tmp_cliques ]
    return map_cliques

def process_clique(clique, superclust, subcenters, connected, npy, threshold):
    sub_indices = []
    #print(clique)
    for ind in clique:
        for  j in superclust[ind]:
            sub_indices.append(j)

    poses = [ subcenters[i] for i in sub_indices ]
    poses = shuffle(poses) #randomize the order of poses
    structures = npy[poses,:,:]
    if len(sub_indices) < 50000:
        clash_matrix, order = sort_clashing(structures, threshold)
        map_cliques = checkclust(structures, sub_indices, order, connected, threshold, clash_matrix)
    else:
        order = range(len(poses))
        map_cliques = checkclust(structures, sub_indices, order, connected, threshold, None)
    return map_cliques

def create_cliques(step, cliques, connected, npy):
    superclust, subcenters, radius = superclusts[step], subcenterss[step], radii[step]
    threshold = cutoff**2 + 2*radius**2
    if 0:
        ###   Sequential (for loop):
        all_map_cliques = []
        for clique in cliques:
            all_map_cliques.append(process_clique(clique, superclust, subcenters, connected, npy, threshold))
    elif 0:
        ###   Sequential (functional programming):
        def process_clique_wrapper(clique):
            return process_clique(clique, superclust, subcenters,  connected, npy, threshold)
        all_map_cliques = map(process_clique_wrapper, cliques)
    else:
        ###   Parallel (multiprocessing)
        import multiprocessing
        workerpool = multiprocessing.Pool()
        #def process_clique_wrapper(clique):
        #    return process_clique(clique, superclust, subcenters, connected, npy, threshold)
        process_clique_wrapper = functools.partial(
            process_clique,
            superclust=superclust,
            subcenters=subcenters,
            connected=connected,
            npy=npy,
            threshold=threshold
        )
        all_map_cliques = workerpool.map(process_clique_wrapper, cliques)

    new_cliques = sum(all_map_cliques, [])
    print("radius = %i    Ncliques = %i"%(radius, len(new_cliques)), file=sys.stderr)
    return new_cliques

# UUU.clust8A.superclust5A: for each 8A-clust, gives the list of indices of 5A-clusters belonging to that 8A-clust.
# UUU.clust8A.subclust5A: contains the 5A-clust obtained from the 8A-clust. No reference to the 8A-clust in that file

if __name__ == '__main__':
    npy_file = sys.argv[1]
    selection_file = sys.argv[2]
    cutoff = float(sys.argv[3]) #cutoff (Angstrom) to consider atoms as clashing
    radii_file = sys.argv[4] #list of clustering radii (Angstrom)
    radii = [float(i) for i in open(radii_file).readlines()[0].split()]
    subcentersfiles =  sys.argv[ 5 : 5 + len(radii)] #"UUU.clust8A, UUU.clust8A.subclust5A", "UUU.clust5A.subclust3A" ...
    superclustfiles = sys.argv[ 5 + len(radii): 5 + 2*len(radii) -1] #"UUU.clust8A.superclust5A", "UUU.clust5A.superclust3A" ...
    npz_file = sys.argv[-1] # UUU-5frag-3A.npz
    ############################
    npy_all = npy2to3(np.load(npy_file)) #np array of all poses coordinates
    sel = [int(i)-1 for i in open(selection_file).readlines()] # poses.list
    npy = npy_all[sel]
    nposes = npy_all.shape[0]
    npz = np.load(sys.argv[-1])
    ############################
    assert len(subcentersfiles) == len(radii), ( len(subcentersfiles) , len(radii) )
    assert len(superclustfiles) == len(radii) - 1, ( len(superclustfiles) , len(radii) - 1 )
    radii.append(0)
    subcenterss = [[int(l.split()[3])-1 for l in open(f).readlines()] for f in subcentersfiles]
    subcenterss.append(range(npy.shape[0]))
    superclusts = [ [range(len(subcenterss[0])) ] ]
    for f in superclustfiles:
        superclusts.append( [ [int(j)-1 for j in l.split()[3:]] for l in open(f).readlines()] )
    if len(subcentersfiles) > 0:
        superclusts.append([[(int(i)-1) for i in l.split()[3:]] for l in open(subcentersfiles[-1]).readlines() ])
    ############################
    sel1_fwd, sel1_bwd = get_sel1(npz, nposes)
    npz = []
    ############################
    #cliques = [[] for i in range(len(superclusts[0]))]
    cliques = [ range(len(superclusts[0])) ]
    for i in range(len(radii)):
        cliques = create_cliques(i, cliques, npy)

    print("out of %i interacting poses"%len(npy), file=sys.stderr)

    for nr, cl in enumerate(cliques):
        print("clique %i => "%(nr+1), end="")
        for i in cl[:-1]:
            print(sel[i]+1, end=" ")
        print(sel[cl[-1]]+1)


'''
def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    poses, interactions =  [], []
    for n in range(nfrags-1):
        inter = npz["interactions-%d"%n]
        interactions.append(inter)
        poses.append(np.unique(inter[:,0]))
    poses.append(np.unique(inter[:,1]))
    #map_interactions = [ poses.index(i), poses.index(i) for [i, j] in interactions ]
    #interactions = [ np.array(i, dtype=int) for i in inter]
    return interactions, poses

interactions_all, poses = map_npz(sys.argv[2]) #x-2frag.npz file from connect.py
nclashes = int(sys.argv[4]) #Nb of atom clashes to consider poses as clashing
poses = [ int(l.split()[0]) for l in open(sys.argv[-2]).readlines() ]
pairs = [np.load(i) for i in sys.argv[5 + 2*len(radii) -1 :]) # pairs of poses that connect at n+1, n+2, n+3
interactions_pooled = set([ i for interaction in interactions_all for i in interaction])
interactions = set( [ [sel.index(i[0]), sel.index(i[1])] for i in interactions_pooled])
s
overlaps = {}
for nr in range(len(poses)):
    fwd = [i for i in range(len(poses)) if poses[i] in interactions[poses[nr]]]
    bwd = [i for i in range(len(poses)) if poses[nr] in interactions[poses[i]]]
    overlaps[nr] = fwd + bwd
'''
