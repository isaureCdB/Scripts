#!/usr/bin/env python3
from __future__ import print_function
import json, sys
'''
concatenate jsonfiles obtained by connecting
selections of poses for each fragment
'''

def map_json(j):
    print("map_json", file = sys.stderr)
    sys.stderr.flush()
    interactions = j['interactions']
    clusters = j["clusters"]
    A = [ i['ranks'][0] for i in clusters[0]]
    B = [ i['ranks'][0] for i in clusters[1]]
    interactions = [ [ A[j[0]], B[j[1]] ] for j in interactions[0] ]
    A = set([ i[0] for i in interactions ])
    B = set([ i[1] for i in interactions ])
    j = [] #free memory
    return clusters, interactions, A, B

def joinjson(jsonlist):
    j = {}
    j['nfrags'] = jsonlist[0]['nfrags']
    j['max_rmsd'] = jsonlist[0]['max_rmsd']
    map_jsonlist = [ map_json(j) for j in jsonlist ]
    print("all jsons mapped", file=sys.stderr)
    sys.stderr.flush()
    int_jsonlist = [ j[1] for j in map_jsonlist ]
    A_jsonlist = [ j[2] for j in map_jsonlist ]
    B_jsonlist = [ j[3] for j in map_jsonlist ]
    del map_jsonlist
    A = list(set.union(*A_jsonlist))
    del A_jsonlist
    print("frag A union computed", file=sys.stderr)
    sys.stderr.flush()
    B = list(set.union(*B_jsonlist))
    del B_jsonlist
    print("frag B union computed", file=sys.stderr)
    sys.stderr.flush()
    A.sort()
    B.sort()
    mapA = {value:ind for ind, value in enumerate(A)}
    mapB = {value:ind for ind, value in enumerate(B)}
    print("frag A and B sorted", file=sys.stderr)
    sys.stderr.flush()
    clusters = []
    ca, cb = [], []
    ca = [ {'radius': 0, 'ranks':[a] } for a in A]
    cb = [ {'radius': 0, 'ranks':[b] } for b in B]
    print("%d + %d clusters constructed" % (len(ca), len(cb)), file=sys.stderr)
    sys.stderr.flush()
    clusters = [ca, cb]
    interactions = [ i for inter in int_jsonlist for i in inter ]
    del int_jsonlist
    print("%d interactions constructed" % len(interactions), file=sys.stderr)
    int_new = [(mapA[i[0]], mapB[i[1]]) for i in interactions]
    j['clusters'] = clusters
    j['interactions'] = int_new
    return j

#jsons = [ json.load(open(i)) for i in sys.argv[1:] ]
jsons = []
for i in sys.argv[1:]:
    j = json.load(open(i))
    print("json loaded", i, file=sys.stderr)
    sys.stderr.flush()
    jsons.append(j)
json_join = joinjson(jsons)
print("writing joined json", file=sys.stderr)
sys.stderr.flush()
json.dump(json_join, sys.stdout)
