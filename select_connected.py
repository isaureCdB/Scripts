#!/usr/bin/env python3

import numpy as np
import sys, threading
from npy import *

'''
extract the list of unique connected poses
'''
npz_file = sys.argv[1]
npz = np.load(npz_file)
nfrags = npz["nfrags"]
poses = set([])
for n in range(nfrags-1):
    inter = npz["interactions-%d"%n]
    poses.update(inter[:,0]+1)
    poses.update(inter[:,1]+1)

for p in poses:
    print(p)
