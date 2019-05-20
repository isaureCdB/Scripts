#!/usr/bin/env python3

import numpy as np
import sys

pdbfilename = sys.argv[1]       # chains[.npy]
cutoff = float(sys.argv[2])     # 2 A

outp1 = pdbfilename + '-clust' + str(cutoff) + '.npy'         # chains-clust2
outp2 = pdbfilename + '-clust' + str(cutoff)

pdb = np.load(pdbfilename+'.npy')
if len(pdb.shape) == 3:
    assert pdb.shape[2] == 3
    pdb = pdb.reshape((pdb.shape[0], 3*pdb.shape[1]))

Nstruc, Ncoor = np.shape(pdb)[0], np.shape(pdb)[1]
struct = list(range(Nstruc))
print("len struct = %i" %(len(struct)))
rmsdtot = [Nstruc*[0] for i in pdb]

for i in range(Nstruc):
    for j in range(i):
        r = ((3/float(Ncoor))*sum([ (pdb[i][a] - pdb[j][a])**2 for a in range(Ncoor)]) )**0.5
        rmsdtot[i][j] = r
        rmsdtot[j][i] = r

print("min max rmsd = %i %i"%(min([min(j) for j in rmsdtot]), max([max(j) for j in rmsdtot])))
rmsd = rmsdtot
centers = []
clusters = []
##
for steps in range(Nstruc*Nstruc):
    maxconnected, maxconnections = 0, 0
    for i in range(len(struct)):
        Nconnections = len( [a for a in rmsd[i] if a <= cutoff] )
#        print "%i connections for struct %i" %(Nconnections,i)
        if Nconnections > maxconnections:
            maxconnected, maxconnections = i, Nconnections
#        print "maxconnected, maxconnections = %i %i" %(maxconnected, maxconnections)
    if maxconnections == 1 or len(struct) == 0:
        print("Converged after "+str(steps)+" steps")
        break
    centers.append(struct[maxconnected])
    clusters.append( [struct[a] for a in range(len(struct)) if rmsd[a][maxconnected] <= cutoff ] )
    struct = [struct[a] for a in range(len(struct)) if rmsd[a][maxconnected] > cutoff]
    rmsd = [[ rmsdtot[a][b] for a in struct] for b in struct ]

centers = centers + struct
clusters = clusters + [ [i] for i in struct]

np.save(outp1, [ pdb[a] for a in centers])

out2 = open(outp2,"w")
for i in range(len(clusters)):
    print("cluster "+str(i+1)+ " -> ", end=' ', file=out2)
    for a in clusters[i]:
        print(a+1, end=' ', file=out2)
    print("", file=out2)

out2.close()

if False:
    rmsdfile = pdbfilename+'.lrmsd'
    rmsdlist = [ float(l.split()[1]) for l in open(rmsdfile).readlines()  ]
    outp3 = pdbfilename + '-clust' + str(cutoff) + '.rmsd-per-clustsize'
    outp4 = pdbfilename + '-clust' + str(cutoff) + '.rmsd-per-rank'
    out3 = open(outp3,"w")
    out4 = open(outp4,"w")
    for j in range(len(centers)):
        print(j+1, rmsdlist[centers[j]], file=out3)

    centers.sort()
    for j in range(len(centers)):
        print(j+1, rmsdlist[centers[j]], file=out4)

    out3.close()
    out4.close()