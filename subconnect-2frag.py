#!/usr/bin/env python3

"""
subconnect.py
Calculates the connections between poses of 2 consecutive fragments based on
_ tight overlap RMSD
_ connections previously computed with large overlap RMSD
Prints out the connectivity tree in JSON format

NOTE: First run get_msd_build.py to build the _get_msd Python extension module

Argument 1: the maximum RMSD
Argument 2: the maximum number of poses to consider (take the first poses in the .postatoms, .preatoms files)
Argument 3: the previously computed connections (npz array)
Argument 4: "preatoms"
Argument 5: "postatoms"
NOTE: the preatoms and postatoms are in .npy format, and must be sorted by ATTRACT rank!
The first pose is rank 1, the 2nd is rank 2, etc.
Argument 6: npz output
Argument 7-8: optional: lists of pose indices to select for each fragment

Copyright 2017-2019 Sjoerd de Vries (INSERM, MTI), Isaure Chauvot de Beauchene (CNRS, LORIA)
"""

import sys, numpy as np
import pyximport
pyximport.install()
from subconnect import subconnect
###################################################
if __name__ == "__main__":
    npz = np.load(sys.argv[1])
    max_rmsd = float(sys.argv[2]) #overlapping cutoff (<3.0A recommended)
    max_msd = max_rmsd**2
    preatoms = np.load(sys.argv[3])
    postatoms = np.load(sys.argv[4])
    outnpz = sys.argv[5]
    nat = preatoms.shape[1] // 3
    # dimensions = (Nb poses, Nb atoms * 3 coordinates)
    preatoms = preatoms.reshape(preatoms.shape[0], nat, 3)
    postatoms = postatoms.reshape(postatoms.shape[0], nat, 3)
    # preatoms and postatoms must have the same number of atoms, as they overlap in sequence.
    assert preatoms.shape[1] == postatoms.shape[1], (n, preatoms.shape, n+1, postatoms.shape)

    connections = npz['interactions-0'].astype(np.int32)
    new_connections = subconnect(preatoms, postatoms, connections, max_msd)
    a = {'max_rmsd': max_rmsd, 'nfrags' : 2}
    a['interactions-0'] = new_connections
    np.savez(outnpz, **a)

'''
    # lists of ranks to consider for each pose pool, counting from 1
    maxstruc = int(sys.argv[2]) #take only the maxstruc top-ranked poses.
    selections = [[] for n in range(nfrags)]
    if len(sys.argv) == 8:
        selections = sys.argv[7:9]
        print >> sys.stderr, "SELECTIONS", selections
        selections = [np.array(sorted([int(l) for l in open(f) if len(l.strip())])) for f in selections]

    #If you use both maxstruc and selection,
    #remove from selection what is beyond rank maxstruc
    if maxstruc > 0:
        for a in (preatoms, postatoms):
            a = a[:maxstruc]
        for selnr, sel in enumerate(selections):
            if not len(sel): continue
            pos = bisect.bisect_right(sel, maxstruc)
            selections[selnr] = sel[:pos]

    # Check that the pose exists for each rank in selection.
    nstruc = [len(preatoms), len(postatoms)]
    for selnr, sel in enumerate(selections):
        for conf in sel:
            assert conf > 0 and conf <= nstruc, (conf, nstruc)

    ranks = [np.arange(s)+1 for s in nstruc]
    if len(selections):
        preatoms = preatoms[selections[0]-1]
        postatoms = postatoms[selections[1]-1]
        ranks = selections
        nstruc = [len(s) for s in selections)

        coor1 = [preatoms[c[0]] for c in connections]
        coor2 = [preatoms[c[1]] for c in connections]
        d = []
        c0 = 0
        for c in connections:
            if c[0] != c0:
                c0 = c[0]
                coor1 = preatoms[c[0]]
            coor2 = postatoms[c[1]]
            msd = get_msd(coor1, coor2)
            print msd.shape
            if msd <= max_msd:
                new_connections.append(c)

'''
