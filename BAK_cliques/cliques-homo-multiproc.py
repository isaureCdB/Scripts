import numpy as np
import sys, threading
from npy import *
import threading
'''
Sort poses into clashing cliques, based on atom-atom distances.
Poses that are connected (in json file) are not considered clashing.
usage: python cliques-greedy-homo-npz.py UUU.npy UUU-6frag-2A.json 1 '5 3 1'\
       UUU.clust5A UUU.clust5A.subclust3A UUU.clust3A.subclust1A \
       UUU.clust5A.superclust3A UUU.clust3A.superclust1A >  UUU-6frag-2A.cliques
'''
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

def checkclust(structures, sub_indices, order, overlaps, threshold, clash_matrix):
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
                if nr1 in overlaps[nr2]:
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

def process_clique(clique, superclust, subcenters, interactions, pool):
    sub_indices = []
    #print(clique)
    for ind in clique:
        #sub_indices = sub_indices + [ i for i in superclust[ind] if subcenters[i] in pool]
        for  j in [ i for i in superclust[ind] if subcenters[i] in pool]:
            sub_indices.append(j)
    poses = [ subcenters[i] for i in sub_indices ]
    overlaps = {}
    for nr in range(len(poses)):
        fwd = [i for i in range(len(poses)) if poses[i] in interactions[poses[nr]]]
        bwd = [i for i in range(len(poses)) if poses[nr] in interactions[poses[i]]]
        overlaps[nr] = fwd + bwd
    structures = npy[poses,:,:]
    if len(sub_indices) < 50000:
        cash_matrix, order = sort_clashing(structures, threshold)
        map_cliques = checkclust(structures, sub_indices, order, overlaps, threshold, cash_matrix)
    else:
        order = range(len(poses))
        map_cliques = checkclust(structures, sub_indices, order, overlaps, threshold, None)
    return map_cliques

def create_cliques(step, cliques, interactions, pool):
    superclust, subcenters, radius = superclusts[step], subcenterss[step], radii[step]
    threshold = cutoff**2 + 2*radius**2
    if 1:
        ###   Sequential (for loop):
        all_map_cliques = []
        for clique in cliques:
            all_map_cliques.append(process_clique(clique, superclust, subcenters, interactions, pool))
    elif 0:
        ###   Sequential (functional programming):
        def process_clique_wrapper(clique):
            return process_clique(clique, superclust, subcenters,  interactions, pool)
        all_map_cliques = map(process_clique_wrapper, cliques)
    else:
        ###   Parallel (multiprocessing)
        import multiprocessing
        workerpool = Pool()
        def process_clique_wrapper(clique):
            return process_clique(clique, superclust, subcenters, interactions, pool)
        all_map_cliques = workerpool.map(process_clique_wrapper, cliques)

    new_cliques = sum(all_map_cliques, [])
    print("radius = %i    Ncliques = %i"%(radius, len(new_cliques)), file=sys.stderr)
    return new_cliques

# UUU.clust8A.superclust5A: for each 8A-clust, gives the list of indices of 5A-clusters belonging to that 8A-clust.
# UUU.clust8A.subclust5A: contains the 5A-clust obtained from the 8A-clust. No reference to the 8A-clust in that file

if __name__ == '__main__':
    npy = npy2to3(np.load(sys.argv[1])) #np array of all poses coordinates
    nstruc = npy.shape[0]
    interactions_all, pool_all = map_npz(sys.argv[2]) #x-2frag.npz file from connect.py
    pool = set([ p for poses in pool_all for p in poses])
    interactions = set()[ i for interaction in  interactions_all for i in interaction])
    cutoff = float(sys.argv[3]) #cutoff (Angstrom) to consider atoms as clashing
    #nclashes = int(sys.argv[4]) #Nb of atom clashes to consider poses as clashing
    radii = [float(i) for i in sys.argv[4].split()] #list of the clustering radius (Angstrom)
    subcentersfiles =  sys.argv[ 5 : 5 + len(radii)] #"UUU.clust8A, UUU.clust8A.subclust5A", "UUU.clust5A.subclust3A" ...
    superclustfiles = sys.argv[ 5 + len(radii):] #"UUU.clust8A.superclust5A", "UUU.clust5A.superclust3A" ...
    assert len(subcentersfiles) == len(radii), ( len(subcentersfiles) , len(radii) )
    assert len(superclustfiles) == len(radii) - 1, ( len(superclustfiles) , len(radii) - 1 )

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
        cliques = create_cliques(i, cliques, interactions, pool)

    print("out of %i interacting poses"%len(pool), file=sys.stderr)

    for nr, cl in enumerate(cliques):
        print("clique %i => "%(nr+1), end="")
        for i in cl[:-1]:
            print(i, end="")
        print(cl[-1])
