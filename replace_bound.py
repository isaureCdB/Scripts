#!/usr/bin/env python3

"""
create list of alternative conf, to replace bound fragments
run from trilib/motif/
"""
import sys, os

def get_clusters(clustfile):
    clusters = []
    for l in open(clustfile).readlines():
        ll = l.split()
        clusters.append( [ int(i)-1 for i in ll[3:] ] )
    #sel = [ c[0] for c in clusters]
    return clusters

def mapping(clusta, clustb): # clust1 clust2.0
    empty_list = []
    alternatives = []
    for nr, ca in enumerate(clusta):
        #print(ca)
        cb = clustb[ca[0]]
        chain = chains[cb[0]]
        #chain2 = sel[nr]
        #assert chain == chain2
        found = False
        for a in ca:
            cb = clustb[a]
            for b in cb:
                if chains[b] != chain:
                    alternatives.append(b + 1)
                    found = True
                    break
            if found:
                break
        if not found:
            alternatives.append("none")
    return alternatives, empty_list

# replace_bound.py confr-fit-clust0.2 confr-fit-clust0.2-clust1.0 UUU chainname.txt confr-fit-clust1.0.sel
cluster02 = get_clusters(sys.argv[1])       # confr-fit-clust0.2
clusters02_1 = get_clusters(sys.argv[2])    # confr-fit-clust0.2-clust1.0
motif = sys.argv[3]                         # UUU
chainname = sys.argv[4]                     # chainname.txt
#selection = sys.argv[5]                     # confr-fit-clust1.0.sel
#sel = [int(l.split()[0]) for l in open(selection).readlines()]

print(len(cluster02), len(clusters02_1))
chains = [l[10:14] for l in open(chainname).readlines()]

alternatives, empty_list = mapping(clusters02_1, cluster02)

f = open(sys.argv[2]+".alternative", "w")
for c in alternatives:
    print(str(c), file=f)
f.close()
