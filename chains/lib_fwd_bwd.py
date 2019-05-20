import sys
import numpy as np
import json
import math

%load_ext Cython

def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    poses, interactions =  [], []
    print(999)
    for n in range(nfrags-1):
        inter = npz["interactions-%d"%n]
        interactions.append(inter)
        poses.append(np.unique(inter[:,0]))
    poses.append(np.unique(inter[:,1]))
    npz = []
    #interactions = [ np.array(i, dtype=int) for i in inter]
    return interactions, poses

def map_json(json_file):
    j = json.load(open(json_file))
    interactions = j['interactions']
    clusters = j['clusters']
    poses = [[ int(i['ranks'][0])-1 for i in cluster] for cluster in clusters]
    mapped_interactions = [[[poses[i][j[0]], poses[i+1][j[1]]] for j in interactions[i]] for i in range(len(interactions))]
    j=[]
    return mapped_interactions, poses

def store_energies(scores_file,RT):
    f = open(scores_file,"r")
    energies = [math.exp(-float(l)/RT) for l in f.readlines()]
    f.close()
    return energies

def fwd(energies, interactions):
    nposes = len(energies)
    nfrags = len(interactions) + 1
    zbar = np.zeros((nfrags,nposes))
    zbar[-1] = 1.0
    for frag in range(nfrags-2, -1,-1):
        for inter in interactions[frag]:
            previouselem = inter[0]
            nextelem = inter[1]
            zbar[frag, previouselem] += energies[nextelem] * zbar[frag+1, nextelem]
    return zbar

def bwd(energies, interactions):
    nposes = len(energies)
    nfrags = len(interactions) + 1
    ybar = np.zeros((nfrags,nposes))
    ybar[0] = 1.0
    for frag in range(1, nfrags):
        for inter in interactions[frag-1]:
            previouselem = inter[0]
            nextelem = inter[1]
            ybar[frag, nextelem] += energies[previouselem]  * ybar[frag-1, previouselem]
    return ybar


'''
def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    clusters, inter =  [], []
    for n in range(nfrags-1):
        inter.append(npz["interactions-%d" % (n)])
    for n in range(nfrags):
        clusters.append(npz["clusters-%d" % (n)])
    npz = []
    p = [[ int(i)-1 for i in cluster] for cluster in clusters]
    interactions = [ np.array([[p[i][j[0]], p[i+1][j[1]]] for j in inter[i]], dtype=int) for i in range(len(inter))]
    return interactions, p
'''
