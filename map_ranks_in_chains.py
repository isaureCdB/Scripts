#!/usr/bin/env python3

import sys

chains_file = sys.argv[1]       # UUU-5frag-2A.chains
ranks_files = sys.argv[2:]      # 1 256
print(len(ranks_files), file=sys.stderr)

ranks = []
for f in ranks_files:
    d = {}
    for l in open(f):
        d[int(l.split()[0])] = int(l.split()[1])
    ranks.append(d)

ll = open(chains_file).readlines()
chains = [l.split() for l in ll[1:]]

if chains[0][0] == "#indices":
    chains = [c[1:] for c in chains]

n = len(chains[1])
print((n-3)*0.5, file=sys.stderr)
nfrag = int((n-3)*0.5)
assert nfrag==len(ranks), (nfrag, len(ranks))

print(ll[0], end="")
for c in chains:
    # print <mean (root-mean-sq) ligand rmsd>
    print(c[0], end=" ")
    # compute <mean (geometric mean) rank>
    gmr = 1
    new_ranks = []
    for i in range(nfrag):
        r = ranks[i]
        p = int(c[3+i])
        new_ranks.append(r[p])
        gmr = gmr*r[p]
    print( int(gmr**(1/nfrag)), end=" ")
    # print  <rms-overlap-rmsd>
    print(c[2], end=" ")
    # print <ranks>
    for r in new_ranks:
        print(r, end=" ")
    # print <ligand rmsds>
    for i in range(3+nfrag, 2+2*nfrag):
        print(c[i], end=" ")
    print(c[-1])
