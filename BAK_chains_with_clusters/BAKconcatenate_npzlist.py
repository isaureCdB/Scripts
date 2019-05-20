#!/usr/bin/env python3
import numpy as np
import sys
'''
concatenate npz files obtained by connecting
selections of poses for each fragment
syntax: concatenate_npzlist.py [list of npz files] --output <outputfile>
'''

def map_npz(npz):
    print("map_npz", file = sys.stderr)
    sys.stderr.flush()
    nfrags = npz["nfrags"]
    assert nfrags == 2
    clusters, interactions =  [], []
    for n in range(nfrags-1):
        interactions.append(npz["interactions-%d" % (n+1)])
    for n in range(nfrags):
        clusters.append(npz["clusters-%d" % (n+1)])
    A, B = clusters[0], clusters[1]
    interactions = [ [ A[i[0]], B[i[1]] ] for i in interactions[0] ]
    A = set([ i[0] for i in interactions ])
    B = set([ i[1] for i in interactions ])
    return interactions, A, B

def join_npz(npzlist):
    npz = {}
    npz['nfrags'] = npzlist[0]['nfrags']
    npz['max_rmsd'] = npzlist[0]['max_rmsd']
    map_npzlist = [ map_npz(npz) for npz in npzlist ]
    print("all npz mapped", file=sys.stderr)
    sys.stderr.flush()
    int_npzlist = [ npz[0] for npz in map_npzlist ]
    A_npzlist = [ npz[1] for npz in map_npzlist ]
    B_npzlist = [ npz[2] for npz in map_npzlist ]
    interactions = np.concatenate(int_npzlist)
    del map_npzlist
    A = list(set.union(*A_npzlist))
    del A_npzlist
    print("frag A union computed", file=sys.stderr)
    sys.stderr.flush()
    B = list(set.union(*B_npzlist))
    del B_npzlist
    print("frag B union computed", file=sys.stderr)
    sys.stderr.flush()
    A.sort()
    B.sort()
    mapA = {value:ind for ind, value in enumerate(A)}
    mapB = {value:ind for ind, value in enumerate(B)}
    print("frag A and B sorted", file=sys.stderr)
    ca = np.array(A)
    cb = np.array(B)
    npz["clusters-1"] = ca
    npz["clusters-2"] = cb
    print("%d + %d clusters constructed" % (len(ca), len(cb)), file=sys.stderr)
    sys.stderr.flush()
    int_new = np.array([(mapA[i[0]], mapB[i[1]]) for i in interactions])
    print("%d interactions constructed" % len(interactions), file=sys.stderr)
    npz['interactions-1'] = int_new
    return npz

assert sys.argv[-2]  == "--output"
output = sys.argv[-1]
npzs = []
for i in sys.argv[1:-2]:
    assert i.endswith(".npz")
    npz = np.load(i)
    print("npz loaded", i, file=sys.stderr)
    sys.stderr.flush()
    npzs.append(npz)
npz_join = join_npz(npzs)
print("writing joined npz", file=sys.stderr)
sys.stderr.flush()
np.savez(output, **npz_join)
