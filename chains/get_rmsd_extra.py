import numpy as np
import sys
from npy import npy2to3, map_npz
###################################################
#actually computes square-deviation (sd), not msd
try:
  import cffi
  import _get_msd
  ffi = _get_msd.ffi
  def get_msd(c1, c2):
    def npdata(a):
      return a.__array_interface__["data"][0]
    nc1, nc2 = len(c1), len(c2)
    natom = c1.shape[1]
    assert c2.shape[1] == natom
    msd = np.empty((nc1, nc2), dtype=float)
    _get_msd.lib.get_msd(
      nc1, nc2, natom,
      ffi.cast("double *", npdata(c1)),
      ffi.cast("double *", npdata(c2)),
      ffi.cast("double *", npdata(msd)),
    )
    return (msd/natom)**0.5
except ImportError:
  print >> sys.stderr, "Cannot find cffi, you will lose some speed"
  def get_msd(c1, c2):
    natom = c1.shape[1]
    d = c1[:, np.newaxis, :, :] - c2[np.newaxis, :, :, :]
    msd = np.einsum("...ijk,...ijk->...i", d,d)
    return (msd/natom)**0.5

interactions = map_npz(sys.argv[1])[0] # UUU-2frags-2A.npz
structures = npy2to3(np.load(sys.argv[2]))
atnucl = int(sys.argv[3]) # len(preatoms)/2 = len(postatoms)/2
nposes = structures.shape[0]

for i, j in interactions:
    rmsd = get_msd(structures[i], structures[j])
    overlap = get_msd(structures[i][atnucl:], structures[j][:2*atnucl])


'''
def map_npz(npz_file):
    print("map_npz",file=sys.stderr)
    sys.stderr.flush()
    npz = np.load(npz_file)
    nfrags = npz["nfrags"]
    clusters, inter =  [], []
    for n in range(nfrags-1):
        inter.append(npz["interactions-%d" % (n)])
    for n in range(nfrags):
        clusters.append(npz["clusters-%d" % (n)])
    npz = []
    p = [[ int(i)-1 for i in cluster] for cluster in clusters]
    interactions = [ np.array([[p[i][j[0]], p[i+1][j[1]]] for j in inter[i]], dtype=int) for i in range(len(inter))]
    return interactions, p
'''
