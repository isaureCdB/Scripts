#!/usr/bin/env python3
import scipy.stats
import json, sys

'''
compare two capri-star sets in format:

    173 all complexes

    top1:  		11 10 5
    top10:  	35 18 9
    top100:  	88 38 15
    top1000:   139 66 22

    121 easy complexes

    top1:  		11 10 5
    top10:  	35 18 9
    top100:  	88 38 15
    top1000:   139 66 22

'''
def get_num_cases(c, ll):
    for l in ll:
        if len(l) < 3:
            continue
        if l[1] == c:
            return int(l[0])
    raise

def get_value(ll, c, t, nstars):
    case = 0
    for l in ll:
        if len(l) < 3:
            continue
        if l[1] == c:
            case = 1
        if l[0] == t+':' and case:
            return int(l[nstars])
    print((ll, c, t, nstars))
    raise

cases = ['all', 'easy', 'medium', 'difficult']
top = ['top1', 'top10', 'top100', 'top1000']
name1 = sys.argv[1]
file1 = sys.argv[2]  #'/home/isaure/benchmarks/benchclean4/systsearch-v100_out-sorted-dr-stars.txt'
name2 = sys.argv[3]
file2 = sys.argv[4]     #'/home/isaure/projets/maria/eros_18-10-2018/capri_stars.txt'
outpjson = sys.argv[5]

data1 = [l.split() for l in open(file1).readlines()]
data2 = [l.split() for l in open(file2).readlines()]

results = {}
for c in cases:
    results[c] = {}
    n = get_num_cases(c, data1)
    for t in top:
        results[c][t] = {}
        for nstars in [1, 2, 3]:
            a = get_value(data1, c, t, nstars)
            e = get_value(data2, c, t, nstars)
            f, p = scipy.stats.fisher_exact([[a, e],[n-a, n-e]])
            d = {}
            d[name1] = a
            d[name2] = e
            d['p-value'] = '%.4f'%p
            results[c][t]['%istars'%nstars] = d

json.dump(results, open(outpjson,'w'), indent = 2, sort_keys = True)
