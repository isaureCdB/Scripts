import sys
import numpy as np
from math import *
from npy import npy2to3

def dist(at1, at2):
    return (sum([ (at1[i] - at2[i])**2 for i in range(3)] ))**0.5

def check(struc1, struc2, cutoff):
    for at1 in struc1:
        for at2 in struc2:
            if dist(at1, at2) < cutoff:
                return True
    return False

clusters = [ [ int(j)-1 for j in l.split()[3:] ] for l in open(sys.argv[1]).readlines() ]
npy = npy2to3(np.load(sys.argv[2]))
cutoff = float(sys.argv[3])

for cl in clusters:
    s = len(cl)
    if s == 1:
        continue
    mat = np.zeros((s,s))
    for i in range(s):
        for j in range(i):
            if check(npy[cl[i]], npy[cl[j]], cutoff):
                mat[i,j] = 1
    percent = 2*np.sum(mat)/(s**2 - s)
    print s, percent
