#!/usr/bin/env python3

import sys, numpy as np

pre = np.load(sys.argv[1])
post = np.load(sys.argv[2])
nmid = 3*int(sys.argv[3])        # nb of overlapping atoms

assert len(pre) == len(post), (len(pre), len(post))
nposes = len(pre)
npre = len(pre[0]) - nmid
npost =  len(post[0]) - nmid
nat = npre + npost + nmid
print((nat, npre, nmid, npost))

tot = np.zeros([nposes, nat])
tot[:, :npost] = post[:, :npost]
tot[:, npost:npost+nmid] = post[:, npost:]
tot[:, npost+nmid:] = pre[:, nmid:]

np.save(sys.argv[4], tot)
