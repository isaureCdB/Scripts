#!/usr/bin/env python3
import sys

lines = open(sys.argv[1]).readlines()

'''
struc = [l[0] for l in ll]
prot = [l[1] for l in ll]
rna = [l[2] for l in ll]
seq = [l[3] for l in ll]
'''
p_struc = "xxxx"
p_prot = "xxxx"
tokeep = []

for ll in lines:
    l = ll.split()
    if len(l) != 4:
        continue
    struc, prot, rna, seq = l
    #Keep only first prot chain per structure
    if struc == p_struc and p_prot != prot:
        continue
    #Compare RNA sequences bound to same or similar prot
    #If one seq contains the other, discard shortest
    if struc[:3] != p_struc[:3]:
        for l1 in tokeep:
            seq1 = l1.split()[3]
            for l2 in tokeep:
                if l1 == l2:
                    continue
                seq2 = l2.split()[3]
                if seq1 in seq2:
                    #print(l1,l2)
                    tokeep.remove(l1)
                    break
                elif seq2 in seq1:
                    #print(l2,l1)
                    tokeep.remove(l2)
        for l in tokeep:
            print(l,end="")
        tokeep = []
    tokeep.append(ll)
    p_struc = struc
    p_prot = prot
