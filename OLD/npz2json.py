import sys
import json
import numpy as np

input, output = sys.argv[1:]
npz = np.load(input)

nfrags = npz['nfrags']
max_rmsd = npz['max_rmsd']
cl = []
for n in range(nfrags):
    a = npz["clusters-%d" % (n)]
    j = [{"ranks": [aa], "radius": 0} for aa in a]
    cl.append(j)
interactions = []
for n in range(nfrags-1):
    a = npz["interactions-%d" % (n)]
    interactions.append(a.tolist())

j = {
    "nfrags": int(nfrags),
    "max_rmsd": float(max_rmsd),
    "clusters": cl,
    "interactions": interactions
}
json.dump(j, open(output, "w"))
