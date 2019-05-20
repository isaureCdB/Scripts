#!/usr/bin/env python3

'''
extend 2-frag connectivity to x-frag connectivity in homopolymers
'''
import sys
import numpy as np

if len(sys.argv) < 3:
    raise Exception("usage: connect-homo.py inp_2frag.npz nfrag outp_nfrag.npz")

j = np.load(sys.argv[1])
nfrag = int(sys.argv[2])
output = sys.argv[3]

print("npz loaded", file = sys.stderr)
sys.stderr.flush()

max_rmsd = j['max_rmsd']
i_ori = np.array(j['interactions-0'])
del j ########################
Ni = len(i_ori)
if isinstance(i_ori[0][0], int) :
    i_ori = i_ori[0]
    Ni = len(i_ori)

A = np.unique(i_ori[:,0])
B = np.unique(i_ori[:,1])

print("%i interactions"%Ni, file=sys.stderr)
sys.stderr.flush()

fwd = { i : [] for i in A }
bwd = { i : [] for i in B }
count = 0
offset = 1000000
while count < Ni:
    for i in i_ori[:offset]:
        fwd[i[0]].append( i[1] )
        bwd[i[1]].append( i[0] )
    count += offset
    print("%d percent interactions processed"%(round(100*count/Ni)), file=sys.stderr)
    i_ori = i_ori[offset:]

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

new_interactions = []
for n in range(len(pools)-1):
    new_inter = np.zeros((Ni,2))
    previous = pools[n]
    count = 0
    for prev in previous:
        for nex in fwd[prev]:
            if nex in pools[n+1]:
                new_inter[count] = [prev, nex]
                count+=1
    new_inter = new_inter[:count]
    print(n, len(new_inter))
    new_interactions.append(new_inter)

print("new_interactions computed", file=sys.stderr)
sys.stderr.flush()

new_interactions2 = []
for n in range(len(new_interactions)):
    new_int = new_interactions[n]
    new_interactions2.append(new_int.astype(int).tolist())
    new_interactions[n] = None #frees numpy array,
    #since there is no variable anymore that refers to it

jout = {}
jout['nfrags'] = nfrag
jout['max_rmsd'] = max_rmsd

for i in range(nfrag-1):
    jout['interactions-%i'%i] = new_interactions2[i]

np.savez(output, **jout)
