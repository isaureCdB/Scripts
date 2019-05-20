#!/usr/bin/env python3
import sys
import numpy as np

'''
../get_surface_beadpairs.py 1GCQAr_acc.pdb 1GCQBr_acc.pdb ipon.npy \
../listBeadPairs-1.4-solutionsList 1GCQ 10 ../list_nb-beadpairs 1.4
'''

pdba = sys.argv[1]          # 1GCQAr_acc.pdb
pdbb = sys.argv[2]          # 1GCQBr_acc.pdb
ipon = np.load(sys.argv[3]) # ipon.npy
goodpairs = sys.argv[4]     # listBeadPairs-1.4-solutionsList
name =  sys.argv[5]         # 1GCQ
rmsd = float(sys.argv[6])   # RMSD cutoff to consider good solutions
Nb_kept = sys.argv[7]       # list_nb-beadpairs
probe = float(sys.argv[8])  # 1.4

ll =  [ l.split() for l in open(Nb_kept).readlines()]
probe_values = [float(i) for i in ll[0]]
col = [nr+1 for nr, i in enumerate(probe_values) if i == probe ][0]
nb_kept = [ l[col+1] for l in ll if l[0] == name][0]

ll = open(pdba).readlines()
acc_a = [ [int(l[57:59]), nr] for nr, l in enumerate(ll) if l[63]=='1']

ll = open(pdbb).readlines()
acc_b = [ [int(l[57:59]), nr] for nr, l in enumerate(ll) if l[63]=='1']

'''
ATOM      1  N   LYS A   1       1.217  -1.500 -23.073   30    1
r1GCQA RANK  7   r 343   l 264   id_BeadPair 6837 RMSD 5.707349   Energy -15.178584
'''
allpairs = [ (i, j) for i in acc_a for j in acc_b ]
all_kept = [ (p[0][1], p[1][1]) for p in allpairs if ipon[p[0][0]-1, p[1][0]-1]==1 ]

print(len(all_kept))

ll = [l.split() for l in open(goodpairs).readlines()]
good = set([(int(l[4]), int(l[6])) for l in ll if l[0][1:5]==name and float(l[10]) <= rmsd])
good_kept = [a for a in all_kept if a in good]

a1, b1, f1 = len(good), int(nb_kept), 1000*len(good)/int(nb_kept)
a2, b2, f2 = len(good_kept), len(all_kept), 1000*len(good_kept)/len(all_kept)

print('1000* %i/%i = %0.2f => 1000* %i/%i = %0.2f good all_kept'%(a1, b1, f1, a2, b2,f2))

#print('good all_kept')
#print([ (i+1, j+1) for (i, j) in good])
#print('good kept')
#print([ (i+1, j+1) for (i, j) in good_kept])
