#!/usr/bin/env python3

import numpy as np
import sys, argparse, json

########################
parser =argparse.ArgumentParser(description=__doc__,
formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('fragments', help="fragments_ori.json")
parser.add_argument('na', help="rna or dna")
parser.add_argument('outp', help="fragments_clust.json")
parser.add_argument('--clustfiles', nargs="+")
parser.add_argument('--clustnames', nargs="+")
args = parser.parse_args()
########################

fragments = json.load(open(args.fragments))
na = args.na

assert len(args.clustnames) == len(args.clustfiles)
clust = zip(args.clustnames, args.clustfiles)

def get_clust(filename):
    print(filename, file=sys.stderr)
    ll = [l.split()[3:] for l in open(filename)]
    clusters = [ l if len(l)>1 else [l[0]] for l in ll]
    return clusters

s = ["C", "A"]
if na == 'dna':
    s = ["G", "T"]

mutations = {'G': 'A', 'U': 'C', 'T': 'C'}
mutpattern = [[a, b, c] for a in [0, 1] for b in [0, 1] for c in [0, 1] ]

def mutate(seq, pattern):
    motif = []
    for i, p in enumerate(pattern):
        m = seq[i]
        if p == 1:
            m = mutations[seq[i]]
        motif.append(m)
    return "".join(motif)

count = 0
for (a, b, c) in [(a, b, c) for a in s for b in s for c in s]:
    motif = a+b+c
    for frag in fragments[motif]:
        for c in args.clustnames:
            fragments[motif][frag]['%i_center'%c] = False
            fragments[motif][frag]['%i'%c] = 0

    dr02 = [l.split() for l in open('%s-%s'%(motif, args.drlist))]
    clust1 =  get_clust('%s-%s'%(motif, args.clustname1))
    clust2 =  get_clust('%s-%s'%(motif, args.clustname2))
    for nd, d in enumerate(dr02):
        center = d[0]
        try:
            fragments[motif][str(center)]['clust0.2A-aa_center'] = True
        except:
            print(motif, center)
            raise
        for frag in d:
            fragments[motif][frag]['clust0.2-aa'] = nd+1
    for nc, cl in enumerate(clust1):
        for c in cl:
            d = dr02[int(c)-1]
            center = dr02[int(cl[0])-1][0]
            fragments[motif][str(center)]['clust1A-aa_center'] = True
            for frag in d:
                fragments[motif][frag]['clust1-aa'] = nc+1
    for nc2, cl2 in enumerate(clust2):
        center_c1 = clust1[ int(cl2[0])-1 ][0]
        center = dr02[int(center_c1)-1][0]
        fragments[motif][str(center)]['clust2A-aa_center'] = True
        for c2 in cl2:
            cl1 = clust1[int(c2)-1]
            for c in cl1:
                d = dr02[int(c)-1]
                for frag in d:
                    fragments[motif][frag]['clust2-aa'] = nc2 + 1

json.dump(fragments, open(args.outp,'w'), indent = 2)
