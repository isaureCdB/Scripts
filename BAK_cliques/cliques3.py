import numpy as np
from numba import jit
import sys
from npy import npy2to3
import threading
from threading import Thread

def inputs(input_list):
    name = input_list[0]
    cutoff = float(input_list[1])
    radii = [ float(i) for i in input_list[2:] ]
    npy = npy2to3(np.load(name+".npy"))
    subclusts =  [ [ int(l.split()[3])-1 for l in open("%s.clust%iA"%(name,radii[0])).readlines() ]]
    superclusts = [ [range(len(subclusts[0])) ] ]
    for i in range(len(radii)-1):
        superclustfile = "%s.clust%iA.superclust%iA"%(name,radii[i], radii[i+1])
        subclustfile = "%s.clust%iA.subclust%iA"%(name,radii[i], radii[i+1])
        superclusts.append( [ [int(j)-1 for j in l.split()[3:]] for l in open(superclustfile).readlines()] )
        subclusts.append( [ int(l.split()[3])-1 for l in open(subclustfile).readlines() ] )

    superclusts.append([ [i] for i in range(npy.shape[0])])
    subclusts.append(range(npy.shape[0]))
    radii.append(0)
    return npy, cutoff, superclusts, subclusts, radii

@jit
def clash(str1, str2, radius):
    threshold = (cutoff + 2 * radius)**2
    for at1 in str1:
        for at2 in str2:
            if np.sum( (at1 - at2)**2 ) < threshold:
                return True
    return False

def checkclust(structures, radius):
    tmp_cliques = []
    for nr1, struc in enumerate(structures):
        new_clique = True
        for nrcl, cl in enumerate(tmp_cliques):
            in_clique = True
            for nr2 in cl:
                if not clash(struc, structures[nr2], 2*radius):
                    in_clique = False
                    break
            if in_clique:
                tmp_cliques[nrcl].append(nr1)
                new_clique = False
                break
        if new_clique:
            tmp_cliques.append([nr1])
    return tmp_cliques

def create_cliques(i, cliques):
    superclust, subclust, radius = zip(superclusts, subclusts, radii)[i]
    print "radius = %i"%radius
    new_cliques = []
    for cl in cliques:
        subclusters = [ l for i in cl for l in superclust[i] ]
        structures = [ npy[subclust[i],:,:] for i in subclusters ]
        new_cliques = new_cliques + checkclust(structures, radius)
    print "Ncliques = %i"%len(new_cliques)
    return new_cliques

if __name__ == '__main__':
    npy, cutoff, superclusts, subclusts, radii = inputs(sys.argv[1:])
    cliques = [ range(len(superclusts[0])) ]

    for i in range(len(radii)):
        cliques = create_cliques(i, cliques)

    dict_cliques = {}
    for nr, cl in enumerate(cliques):
        dict_cliques[nr] = cl

    json.dump(dict_cliques, open(sys.argv[-1]))
