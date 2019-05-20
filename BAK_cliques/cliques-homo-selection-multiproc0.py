#!/usr/bin/env python3
import numpy as np
import sys, threading, argparse
from npy import *
import threading
import functools
'''
Sort poses into clashing cliques, based on atom-atom distances.
Poses that are connected at (n,n+1), (n,n+2) or (n,n+3) do not clash.
x = UUU-6frag-2A
usage: python cliques-greedy-homo-npz.py x.npy connected.sel clash-cutoff '5 3 1'\
       x.clust5A x.clust5A.subclust3A x.clust3A.subclust1A \
       x.clust5A.superclust3A x.clust3A.superclust1A mapnpz-outp.npz >  UUU-6frag-2A.cliques
See cliques-homo-selection-multiproc.sh for proper usage
'''

if len(subcenters) == nsel: # we are at the singleton level
        connected = get_connected(poses, indices, sel1_fwd, sel1_bwd)# list of sets

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
    exception = [[] for n in structures]
    if threshold = cutoff**2:  # we are at the singleton level of clustering
        exception = connected
        print("singleton level", file = sys.stderr)
    tmp_cliques = []
    for nr1 in order:
        struc1  = structures[nr1]
        new_clique = True
        ''' check for each clique if struc1 can belong to it'''
        for nrcl, cl in enumerate(tmp_cliques):
            in_clique = True
            '''check for each pose in clique if struc1 clashes with it'''
            for nr2 in cl:
                ''' poses that are connected don't clash'''
                if nr1 in exception[nr2]:
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
    npy_all = npy2to3(np.load(sys.argv[1])) #np array of all poses coordinates
    sel = [int(i)-1 for i in open(sys.argv[2]).readlines()] # connected poses list
    cutoff = float(sys.argv[3]) #cutoff (Angstrom) to consider atoms as clashing
    radii = [float(i) for i in open(sys.argv[4]).readlines()[0].split()] #list of clustering radii (Angstrom)
    subcentersfiles =  sys.argv[ 5 : 5 + len(radii)] #"UUU.clust8A, UUU.clust8A.subclust5A", "UUU.clust5A.subclust3A" ...
    superclustfiles = sys.argv[ 5 + len(radii): 5 + 2*len(radii) -1] #"UUU.clust8A.superclust5A", "UUU.clust5A.superclust3A" ...
    connected = np.load(sys.argv[-1]) # pairs123.npy: connected poses at n+1,+2,+3
    npy = npy_all[sel]

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

    #cliques = [[] for i in range(len(superclusts[0]))]
    cliques = [ range(len(superclusts[0])) ]
    for i in range(len(radii)):
        cliques = create_cliques(i, cliques, connected, npy)

    print("out of %i interacting poses"%len(npy), file=sys.stderr)

    for nr, cl in enumerate(cliques):
        print("clique %i => "%(nr+1), end="")
        for i in cl[:-1]:
            print(sel[i]+1, end=" ")
        print(sel[cl[-1]]+1)


'''
    ############
    parser =argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('coor', help="poses coordinates", type=np.load)
    parser.add_argument('cutoff', help="cutoff", type=float)
    parser.add_argument('clustfiles', help="cutoff", type=float)
    parser.add_argument("--connected", help="dict of connected poses", type=np.load)
    parser.add_argument("--connections", help="connections tree", type=np.load)
    args = parser.parse_args()
    ############
'''
