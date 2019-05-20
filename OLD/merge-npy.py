import numpy as np
import sys
from npy import npy2to3

'''
BUGGED !!!
'''
print >> sys.stderr, "bugged"
sys.exit()

def reshape(npy):
    reshape = False
    if len(npy.shape) == 3:
        assert npy.shape[2] == 3
    else:
        assert len(npy.shape) == 2 and npy.shape[1]%3 == 0
        npy = npy.reshape(npy.shape[0],npy.shape[1]/3,3)
        reshape = True
    return npy, reshape

a_npy = np.load(sys.argv[1])
b_npy = np.load(sys.argv[2])
aatoms = [int(l.split()[0])-1 for l in open(sys.argv[3]).readlines()[1:]]
batoms = [int(l.split()[0])-1 for l in open(sys.argv[4]).readlines()[1:]]

if aatoms[0] < batoms[0]:
    pre_npy, post_npy = b_npy, a_npy
    preatoms, postatoms = batoms, aatoms
else:
    pre_npy, post_npy = a_npy, b_npy
    preatoms, postatoms = aatoms, batoms

pre_npy, preshape = npy2to3(pre_npy)
post_npy, postshape = npy2to3(post_npy)

postlist = [i for i in postatoms if i not in preatoms]
post = post_npy[:,postlist,:]

print >> sys.stderr, post.shape
print >> sys.stderr, pre_npy.shape

tot = np.concatenate((post, pre_npy),axis=1)

if preshape:
    tot = tot.reshape(tot.shape[0],tot.shape[1]*3)

np.save(sys.stdout, tot)
