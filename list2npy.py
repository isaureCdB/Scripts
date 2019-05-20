#!/usr/bin/env python3

import numpy as np, sys, argparse

ll = [ l.split() for l in open(sys.argv[1])]
a = np.array([[float(i) for i in l] for l in ll if len(l) > 0], dtype="float32")

outp = sys.argv[1] + '.npy'
if len(sys.argv) > 2:
    outp = sys.argv[2]

np.save(outp, a)
