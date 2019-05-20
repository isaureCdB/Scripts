#!/usr/bin/env python3

import numpy as np
import sys

'''
usage : percent_clash_chains.py <rmsd> <mindist> <nfrag> <spacing> [<occurancies>]
'''
rmsdfile = sys.argv[1]
mindist_file = [ l for l in open(sys.argv[2]).readlines() if not l.startswith("#")]
mindist_all = np.array([ [float(i) for i in l.split()[1:]] for l in mindist_file])
nchain = mindist_all.shape[0]
nfrag = int(sys.argv[3])
spacing = int(sys.argv[4]) # minimal spacing
if False:
#if len(sys.argv) > 5 :
    occurencies = np.array( [int(l.split()[0]) for l in open(sys.argv[5]).readlines()])
else:
    occurencies = np.ones(nchain)
nchain = sum(occurencies)
print(nchain, file=sys.stderr)


cutoffs = [ int(i) for i in [3, 4, 5, 6, 8, 10]]
ndist = len([j for i in range(nfrag-spacing) for j in range(i+spacing, nfrag)])
assert mindist_all.shape[1] == ndist, (mindist_all.shape[1], ndist)

dist = {s:[] for s in range(spacing, nfrag)}
count = 0
for i in range(nfrag-spacing):
    for j in range(i+spacing, nfrag):
        dist[j-i].append(count)
        count+=1

print(dist, file=sys.stderr)

percent = {}
rmsd = np.array([float(l.split()[1]) for l in open(rmsdfile).readlines()])
for i in [5, 4]:
    inf = ( (rmsd < (i + 0.05)) * occurencies).sum()
    percent[i] = 100 * float(inf) / sum(occurencies)

print("# <spacing> <clash-cutoff> <infx> <% clashing> <% near-native total> <% near-native no-clash> <enrichment>")
for s in range(spacing, nfrag): # spacing
    mindist = mindist_all[:, dist[s]]
    for c in cutoffs:    # clash cutoff
        noclash = np.min(mindist, axis=1) > c
        N_noclash = float(sum(noclash*occurencies))
        if N_noclash == 0:
            continue
        print("spacing %i, cutoff %i : %i N_noclash"%(s, c, N_noclash),file=sys.stderr)
        for i in [4, 5]:    # near-native cutoff
            N_noclash_inf = sum((rmsd[noclash] < i+0.05)*(occurencies[noclash]))
            new_percent = 100 *  N_noclash_inf/N_noclash
            if percent[i] == 0:
                increase = 0
            else:
                increase = new_percent / percent[i]
            clashing = 100 - 100*(N_noclash/nchain)
            print("%i %i %i %.2f %.2f %.2f %.2f" %(s, c, i, clashing, percent[i], new_percent, increase))
