
#!/usr/bin/env python3
import json, sys
import numpy as np

npz = np.load(sys.argv[1])
nfrag = int(sys.argv[2])
print("npz loaded", file = sys.stderr)
sys.stderr.flush()
outputfile = sys.argv[3]

max_rmsd = npz['max_rmsd']
cl = []
for n in range(2):
    cl.append(npz["clusters-%d" % (n+1)])
i_ori = []
for n in range(1):
    i_ori.append(npz["interactions-%d" % (n+1)])

Ni = len(i_ori)
if not isinstance(i_ori[0][0], int) :
    i_ori = i_ori[0]
    Ni = len(i_ori)

print("%i interactions"%Ni, file=sys.stderr)
sys.stderr.flush()

A = cl[0]
B = cl[1]

fwd = { i : [] for i in A }
bwd = { i : [] for i in B }
for j, i in enumerate(i_ori):
    fwd[ A[i[0]] ].append( B[i[1]] )
    bwd[ B[i[1]] ].append( A[i[0]] )
    if not (j%5000000):
        print("%d percent interactions processed"%(round(100*j/Ni)), file=sys.stderr)

del i_ori #########################

Aset = set(A)
del A #########################
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

Bset = set(B)
del B #########################
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

pools_dict = { i : pools[i] for i in range(nfrag)}

clust = []
for i in range(nfrag):
    pool = pools[i]
    c = []
    for pose in pool:
        c.append({'ranks':[pose], 'radius':0})
    clust.append(c)
    print("%i connected poses for frag %i "%(len(c),i+1) , file = sys.stderr)

sys.stderr.flush()

clust_dict = { i : clust[i] for i in range(nfrag)}

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

new_interactions2 = []
for n in range(len(new_interactions)):
    new_int = new_interactions[n]
    new_interactions2.append(new_int.astype(int).tolist())
    new_interactions[n] = None #frees numpy array,
    #since there is no variable anymore that refers to it

arrays = {
    "nfrags": np.array(nfrag),
    "max_rmsd": np.array(max_rmsd)
}
for dnr, d in enumerate(clust):
    ar = np.array([dd["ranks"][0] for dd in d])
    arrays["clusters-%d" % (dnr+1)] = ar
for dnr, d in enumerate(new_interactions2):
    ar = np.array(d)
    arrays["interactions-%d" % (dnr+1)] = ar
np.savez(outputfile, **arrays)