#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Find all interface residues
Created on Wed Jun 12 13:14:50 2013

modified from @author: christina
"""
import sys
import numpy as np
from scipy.spatial.distance import cdist

def read_struc(file1):
    atomlist = []
    for line in open(file1).readlines():
        if not line.startswith('ATOM'):
            continue
        x,y,z = (float(f) for f in (line[30:38],line[38:46],line[46:54]))
        item = (int(line[4:11]),int(line[22:26]), x, y, z)
        atomlist.append(item)
    return atomlist

def read_multi_struc(file2):
    for line in open(file2).readlines():
        if line.startswith('MODEL'):
            atomlist.append([])
        if not line.startswith('ATOM'):
            continue
        x,y,z = (float(f) for f in (line[30:38],line[38:46],line[46:54]))
        item = (int(line[4:11]),int(line[22:26]), x, y, z)
        atomlist[-1].append(item)
    return atomlist

def get_interface(a1, a2, rcut):
    crd1 = [[x,y,z] for name, res, x,y,z in a1]
    crd1 = np.matrix(crd1)
    crd2 = [[x,y,z] for name, res, x,y,z in a2]
    crd2 = np.matrix(crd2)
    Y = cdist(crd1,crd2,'euclidean')
    contacts = []
    for i in range(len(a1)):
      res1 = a1[i][1]
      for j in range(len(a2)):
	        res2 = a2[j][1]
	        dist = Y[i][j]
	        if dist < rcut:
	          if not (res1,res2) in contacts:
	            print("%i %i %.2f"%(res1, res2, dist))
	            contacts.append((res1,res2))


rcut = float(sys.argv[3])
a1 = read_struc(sys.argv[1])
a2 = read_struc(sys.argv[2])
n1 = sys.argv[1].split(".pdb")[0]
n2 =sys.argv[2].split(".pdb")[0]
get_interface(a1, a2, rcut)
