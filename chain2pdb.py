#!/usr/bin/env python3

'''
convert text-file chains of fragments into multi-models pdb:
    1 PDB-file per chain
    1 model per fragment
writes in <input_name>-x.pdb

usage: chain2pdb.py <chains> --npy <motif[1-m].npy> --pdb <motif[1-m].pdb>
'''

import sys, numpy as np, argparse
from npy import npy2to3

def convert_monostruct(npy, template, m):
    assert len(template) == npy.shape[0], (len(template), npy.shape)
    lines = []
    for nl, l in enumerate(template):
        coor = npy[nl]
        lines.append(l[:30]+"%8.3f%8.3f%8.3f"%(coor[0], coor[1], coor[2])+l[54:-1])
    return lines

def parse_template(template):
    parsed = []
    for l in open(template).readlines():
        if l.startswith("ATOM") or l.startswith("HETATM"):
            parsed.append(l)
    return parsed

#######################################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('chains_file', help="UUU-5frag-2A.chains outp from assembly")
parser.add_argument('--npy', help="UUU-aa.npy as fragment poses", nargs='+')
parser.add_argument('--pdb', help="UUU.pdb as template", nargs='+')

# obsolete option (to merge, use SCRIPTS/chains2rna.py)
parser.add_argument('--fragments', help="output: chains of fragments", action="store_true")
parser.add_argument("--merged",help="output: chains of merged coordinates", action="store_true")

args = parser.parse_args()
#######################################

chains_file = args.chains_file      # UUU-5frag-2A.chains
npy_poses = [npy2to3(np.load(f)) for f in args.npy ]     # UUU-aa.npy
templates = [ parse_template(f) for f in args.pdb ]

chains = [l.split() for l in open(chains_file)]
if chains[1][0] == "#indices":
    chains = [c[1:] for c in chains]

n = len(chains[1])
print((n-3)*0.5, file=sys.stderr)
nfrag = int((n-3)*0.5)
assert nfrag==len(npy_poses), (nfrag, len(npy_poses))

for nc, chain in enumerate(chains[1:]):
    outp = open('%s-%i.pdb'%(args.chains_file, nc+1),'w')
    for i in range(nfrag):
        pose = int(chain[3+i])
        npy = npy_poses[i][pose-1]
        print(npy.shape)
        templ = templates[i]
        new_lines = convert_monostruct(npy, templ, i+1)
        print("MODEL %i"%(i+1), file = outp)
        for l in new_lines:
            print(l, file = outp)
        print("ENDMDL", file = outp)
    outp.close()
