#!/usr/bin/env python3
import numpy as np
import sys
'''
concatenate npz files obtained by connecting
selections of poses for each of 2 fragments
syntax: concatenate_npzlist.py [list of npz files] --output <outputfile>
'''

def map_npz(npz):
    print("map_npz", file = sys.stderr)
    sys.stderr.flush()
    nfrags = npz["nfrags"]
    assert nfrags == 2
    interactions = npz["interactions-0"]
    return interactions

def join_npz(npzlist):
    npz = {}
    npz['nfrags'] = npzlist[0]['nfrags']
    npz['max_rmsd'] = npzlist[0]['max_rmsd']
    paires_npzlist = [ map_npz(npz) for npz in npzlist ]
    print("all npz mapped", file=sys.stderr)
    sys.stderr.flush()
    pairs = np.concatenate(paires_npzlist)
    npz['interactions-0'] = np.unique(pairs)
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
