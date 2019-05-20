#!/usr/bin/env python
import sys, os, argparse
import numpy as np
import itertools
#######################################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pdbfile', help="(list of) unbound pdb")
parser.add_argument('reference', help="reference pdb structure")
parser.add_argument("--list",help="input is a list of files", action="store_true")
parser.add_argument("--multipdb",help="input is a multipdb", action="store_true")
parser.add_argument("--ref", default=None, help="additional reference")
parser.add_argument("--sym", default=None, help="symetrical atoms")
parser.add_argument("--atoms", default=None, help="name of atoms to consider", nargs="+")

args = parser.parse_args()
#######################################

def rmsd(refcoord, atoms2, symertical):
    rmsd = []
    for atoms1 in refcoord:
        assert len(atoms1) == len(atoms2), (len(atoms1), len(atoms2))
        assert len(atoms1) > 0
        d = atoms1 - atoms2
        d2 = d * d
        sd = d2.sum(axis = 1)
        if len(symertical) > 0:
            for sym in symertical:
                coor1 = atoms1[sym]
                coor2 = atoms2[sym]
                diff = np.sum((coor1[None,:] - coor2[:,None])**2, axis = 2)
                rmin = 10000
                for perm in itertools.permutations(range(len(sym))):
                    r = np.sum(diff[i,perm[i]] for i in range(len(sym)))
                    if r < rmin:
                        rmin = r
                        dmin = [ diff[i,perm[i]] for i in range(len(sym)) ]
                for i in range(len(sym)):
                    sd[sym[i]] = dmin[i]
        rmsd.append(np.sqrt(sd.mean()))
    return np.min(rmsd)

if args.list:
    pdbs = [ l.split()[0] for l in open(args.pdbfile).readlines()]
else:
    pdbs = [args.pdbfile]

references = [ open(args.reference).readlines() ]
if args.ref:
    references.append( open(args.ref).readlines() )

structures = [[ l for l in open(pdb).readlines() ] for pdb in pdbs ]
refatoms = [[ l for l in ref if l.startswith("ATOM")] for ref in references]

if args.atoms is not None:
    print(args.atoms)
    structures  = [[ l for l in s if str(l[11:17]).strip() in args.atoms] for s in structures]
    refatoms  = [[ l for l in ref if str(l[11:17]).strip() in args.atoms] for ref in refatoms]

if args.multipdb:
    models = []
    for struc in structures:
        for l in struc:
            if l.startswith("MODEL"):
                models.append([])
            if l.startswith("ATOM"):
                models[-1].append(l)
    structures = models
else:
    structures = [ [ l for l in s if l.startswith("ATOM")] for s in structures ]


symetrical = []
if args.sym != None:
    symetrical = [ [int(j)-1 for j in l.split()] for l in open(args.sym).readlines()]


refcoord = [np.array([ [float(i) for i in [l[30:38], l[38:46], l[46:54]] ] for l in atoms1 ]) for atoms1 in refatoms]
structcoord = [ np.array([ [float(i) for i in [l[30:38], l[38:46], l[46:54]] ] for l in atoms2 ]) for atoms2 in structures]

count = 1
for coord in structcoord:
    print count, rmsd(refcoord, coord, symetrical)
    count+=1
