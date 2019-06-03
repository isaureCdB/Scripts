#!/usr/bin/env python3

import numpy as np
import sys
'''
usage: npy2dat file.dat.header file.dat.npy --conf file.dat.ens --ene file.dat.ene > file.dat
reverse process from "dat2npy.py"
'''

header = open(sys.argv[1]).readlines()
for l in header:
    print(l, end=' ')

data = np.load(sys.argv[2])

count = 0
for struc in data:
    count+=1
    print("#%i"%count)
    print("## Energy: %d"%struc[0])
    print(" 0.000000 0.000000 -0.000000 0.0000 -0.0000 0.0000")
    for j in struc[1:7]:
        print(" %s"%j, end=' ')
    print(" %s"%struc[7])
