#!/usr/bin/env python3
import sys, argparse

def count_atom(pdb):
    count_atom_pdb = 0
    for l in pdb:
        if l.startswith("ATOM") or l.startswith("HETATM"):
            count_atom_pdb +=1
        if l.split()[0] == "MODEL" and l.split()[1] == 2:
            return count_atom_pdb
    return count_atom_pdb

def count_bfact(bfact):
    count_bfact_pdb = 0
    for l in bfact:
        if not l.startswith("MODEL"):
            count_bfact_pdb +=1
        if l.split()[0] == "MODEL":
            if l.split()[1] == 2:
                return count_bfact_pdb
    return count_bfact_pdb

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pdb_file')
parser.add_argument('bfact_file')
args = parser.parse_args()
#######################

pdb = open(args.pdb_file).readlines()
bfact = open(args.bfact_file).readlines()

assert count_atom(pdb) == count_bfact(bfact)
nmodels_pdb = len([l for l in pdb if l.startswith("MODEL")])
nmodels_bfact = len([l for l in bfact if l.startswith("MODEL")])

if nmodels_bfact > 0:
    assert nmodels_bfact == nmodels_pdb

count = 0
for l in pdb:
    if l.startswith("MODEL"):
        count += 1
        if nmodels_bfact == 0:
            count = 0
    if not (l.startswith("ATOM") or l.startswith("HETATM")) :
        print(l, end="")
        continue
#    print((count, bfact[count]), file=sys.stderr)
    print("%s%.2f"%(l[:61], float(bfact[count])))
    count += 1
