import numpy as np
#from numba import jit
import sys
from npy import npy2to3
import threading
import json

def read_json(jsonfile, nstruc):
    j = json.load(open(jsonfile))
    clusters = j["clusters"]
    interactions_ori = j['interactions']
    del j
    poses_lists = [ [int(i['ranks'][0])-1 for i in cl] for cl in clusters ]
    del clusters
    interactions = { i : [] for i in range(nstruc) }
    for nr, i_ori in enumerate(interactions_ori):
        for j, i in enumerate(i_ori):
            interactions[ poses_lists[nr][i[0]] ].append( poses_lists[nr+1][i[1]] )
            interactions[ poses_lists[nr+1][i[1]] ].append( poses_lists[nr][i[0]] )
    del poses_lists
    return interactions

#@jit
def clash(str1, str2, radius):
    threshold = (cutoff + 2*radius)**2
    for at1 in str1:
        for at2 in str2:
            if np.sum( (at1 - at2)**2 ) < threshold:
                return True
    return False

def checkclust(structures, indexes, radius, new_cliques, overlaps):
    tmp_cliques = []
    for nr1, struc1 in enumerate(structures):
        if len(overlaps[indexes[nr1]]) == 0:
            continue
        new_clique = True
        ''' check for each clique if struc1 can belong to it'''
        for nrcl, cl in enumerate(tmp_cliques):
            in_clique = True
            for nr2 in cl:
                ''' if poses are overlaping, they can't be in same clique'''
                if indexes[nr1] in overlaps[indexes[nr2]]:
                    in_clique = False
                    break
                struc2 = structures[nr2]
                ''' if poses can't clash, they can't be in same clique'''
                if not clash(struc1, struc2, radius):
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
    map_cliques = [ [indexes[i] for i in cl] for cl in tmp_cliques ]
    return map_cliques

def create_cliques(step, cliques, interactions):
    superclust, subclust, radius = superclusts[step], subclusts[step], radii[step]
    new_cliques = []
    for cl in cliques:
        subclusters = [ l for i in cl for l in superclust[i] if l in interactions.keys() ]
        structures = [ npy[subclust[i],:,:] for i in subclusters ]
        overlaps = {}
        for pose in subclusters:
            overlaps[pose] = [ i for i in interactions[pose] if i in subclusters]
        new_cliques = new_cliques + checkclust(structures, subclusters, radius, new_cliques, overlaps)
    print >> sys.stderr, "radius = %i    Ncliques = %i"%(radius, len(new_cliques))
    return new_cliques

if __name__ == '__main__':
    npy = npy2to3(np.load(sys.argv[2]))
    nstruc = npy.shape[0]
    interactions = read_json(sys.argv[1], nstruc)
    cutoff = float(sys.argv[3])
    radii = [float(i) for i in sys.argv[4].split()]
    subclustfiles =  sys.argv[ 5 : 4 + len(radii)]
    superclustfiles = sys.argv[ 4 + len(radii):]

    subclusts = [ [ int(l.split()[3])-1 for l in open(f).readlines() ] for f in subclustfiles ]
    subclusts.append(range(npy.shape[0]))
    superclusts = [ [range(len(subclusts[0])) ] ]
    for f in superclustfiles:
        superclusts.append( [ [int(j)-1 for j in l.split()[3:]] for l in open(f).readlines()] )
    if len(subclustfiles) > 0:
        superclusts.append( [ [(int(i)-1) for i in l.split()[3:]] for l in open(subclustfiles[-1]).readlines() ] )

    cliques = [ range(len(superclusts[0])) ]

    for i in range(len(radii)):
        cliques = create_cliques(i, cliques, interactions)

    for nr, cl in enumerate(cliques):
        print "clique %i => "%(nr+1),
        for i in cl[:-1]:
            print i,
        print cl[-1]
