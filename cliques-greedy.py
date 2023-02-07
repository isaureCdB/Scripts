import numpy as np
#from numba import jit
import sys
from npy import npy2to3
import threading
import json
'''
Sort poses into clashing cliques, based on atom-atom distances.
Poses that are connected (in json file) are not considered clashing.
'''
def read_json(jsonfile, nstruc):
    j = json.load(open(jsonfile))
    clusters = j["clusters"]
    interactions_ori = j['interactions']
    del j
    poses = [ [int(i['ranks'][0])-1 for i in cl] for cl in clusters ]
    del clusters
    interactions = { i : [] for i in range(nstruc) }
    for nr, i_ori in enumerate(interactions_ori):
        for j, i in enumerate(i_ori):
            interactions[ poses[nr][i[0]] ].append( poses[nr+1][i[1]] )
            interactions[ poses[nr+1][i[1]] ].append( poses[nr][i[0]] )
    poses = set([ i for p in poses for i in p])
    return interactions, poses

def get_clashes(structures, threshold):
    import cffi
    from _get_clashes import ffi
    from _get_clashes.lib import get_clashes
    def npdata(a):
      return a.__array_interface__["data"][0]
    n = structures.shape[0]
    nat = structures.shape[1]
    clash_matrix = np.zeros((n, n), dtype = bool)
    ptr_structures = ffi.cast("double *", npdata(structures) )
    ptr_matrix = ffi.cast("bool *", npdata(clash_matrix) )
    get_clashes(n, nat, threshold, ptr_structures, ptr_matrix)
    return clash_matrix

def sort_clashing(structures, threshold):
    n = structures.shape[0]
    tmp_cliques = []
    clash_matrix = get_clashes(structures, threshold)
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
                    if not get_clashes(struc, threshold)[0, 0]:
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

def create_cliques(step, cliques, interactions, pool):
    superclust, subcenters, radius = superclusts[step], subcenterss[step], radii[step]
    threshold = cutoff**2 + 2*radius**2
    new_cliques = []
    for clique in cliques:
        sub_indices = []
        print >> sys.stderr, len(clique)
        for ind in clique:
            sub_indices = sub_indices + [ i for i in superclust[ind] if subcenters[i] in pool]
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
        new_cliques = new_cliques + map_cliques
    print >> sys.stderr, "radius = %i    Ncliques = %i"%(radius, len(new_cliques))
    return new_cliques

if __name__ == '__main__':
    npy = npy2to3(np.load(sys.argv[1]))
    nstruc = npy.shape[0]
    interactions, pool = read_json(sys.argv[2], nstruc)
    cutoff = float(sys.argv[3])
    radii = [float(i) for i in sys.argv[4].split()]
    subcentersfiles =  sys.argv[ 5 : 4 + len(radii)]
    superclustfiles = sys.argv[ 4 + len(radii):]

    subcenterss = [[int(l.split()[3])-1 for l in open(f).readlines()] for f in subcentersfiles]
    subcenterss.append(range(npy.shape[0]))
    superclusts = [ [range(len(subcenterss[0])) ] ]
    for f in superclustfiles:
        superclusts.append( [ [int(j)-1 for j in l.split()[3:]] for l in open(f).readlines()] )
    if len(subcentersfiles) > 0:
        superclusts.append([[(int(i)-1) for i in l.split()[3:]] for l in open(subcentersfiles[-1]).readlines() ])

    cliques = [ range(len(superclusts[0])) ]

    for i in range(len(radii)):
        cliques = create_cliques(i, cliques, interactions, pool)

    print >> sys.stderr, "out of %i interacting poses"%len(pool)

    for nr, cl in enumerate(cliques):
        print "clique %i => "%(nr+1),
        for i in cl[:-1]:
            print i,
        print cl[-1]
