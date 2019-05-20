#!/usr/bin/env python3
'''
extend 2-frag connectivity to x-frag connectivity in homopolymers
'''
import json, sys
import numpy as np

npz = np.load(sys.argv[1])
print("npz loaded", file = sys.stderr)
sys.stderr.flush()
nfrag = int(sys.argv[2])
outputfile = sys.argv[3]

max_rmsd = npz['max_rmsd']
pairs = npz["interactions-0"]

Aset = set([p[0] for p in pairs])
Bset = set([p[1] for p in pairs])

Ni = len(pairs)
print("%i interactions"%Ni, file=sys.stderr)
sys.stderr.flush()

fwd = [ [p[1] for p in pairs if p[0] == a] for a in Aset ]
bwd = [ [p[0] for p in pairs if p[1] == b] for b in Bset ]

fwd_poses = [Aset]
for f in range(nfrag-1):
    targets = set()
    for ori in fwd_poses[-1]:
        if ori not in Aset:
            continue
        target = fwd[ori]
        targets.update(target)
    fwd_poses.append(targets)

print("fwd connections computed", file=sys.stderr)
sys.stderr.flush()

bwd_poses = [Bset]
for f in range(nfrag-1):
    oris = set()
    for target in bwd_poses[-1]:
        if target not in Bset:
            continue
        ori = bwd[target]
        oris.update(ori)
    bwd_poses.append(oris)

del bwd #########################
print("bwd connections computed", file=sys.stderr)
sys.stderr.flush()

pools = []
for i in range(nfrag):
    l = list(fwd_poses[i] & bwd_poses[nfrag-1-i])
    l.sort()
    pools.append(l)

print("intersection of bwd-fwd connections done", file=sys.stderr)
sys.stderr.flush()

new_interactions = []
for n in range(len(pools)-1):
    new_inter = np.zeros((Ni,2))
    previous = pools[n]
    count = 0
    next = { value:ind for ind, value in enumerate(pools[n+1])}
    for i1 in range(len(previous)):
        for target in fwd[previous[i1]]:
            if target in next:
                i2 = next[target]
                new_inter[count] = [i1, i2]
                count+=1
    new_inter = new_inter[:count]
    new_interactions.append(new_inter)

print("new_interactions computed", file=sys.stderr)
sys.stderr.flush()

'''
new_interactions2 = []
for n in range(len(new_interactions)):
    new_int = new_interactions[n]
    new_interactions2.append(new_int.astype(int).tolist())
    new_interactions[n] = None #frees numpy array,
    #since there is no variable anymore that refers to it
'''

arrays = {
    "nfrags": np.array(nfrag),
    "max_rmsd": np.array(max_rmsd)
}

for dnr, d in enumerate(new_interactions):
    ar = np.array(d)
    arrays["interactions-%d" % dnr] = ar
np.savez(outputfile, **arrays)
