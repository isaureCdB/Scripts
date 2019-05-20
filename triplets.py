import sys

pdb = open(sys.argv[1])
name = sys.argv[2]

res = []
resid = None
for l in pdb:
    if not l.startswith("ATOM"):
        continue
    if int(l[22:26]) != resid:
        res.append([])
        resid = int(l[22:26])
    res[-1].append(l)

for i in range(len(res)-2):
    outp = open("%s%d-%dr.pdb"%(name,i+1,i+3), "w")
    for r in res[i:i+3]:
        for j in r:
            print >> outp, j,


