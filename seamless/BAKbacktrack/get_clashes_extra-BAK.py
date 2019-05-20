'''
detect which chains of poses have clashes for any pair of fragments (f,f+i) with i>2
usage: python get_clashes_extra.py chains.txt <cutoff in A> <mapping> <motif1.npy> <motif2.npy>
<mapping> : string mapping fragments to motifs.
            ex: for a UAUAUA sequence, use "0 1 0 1" with UAU.npy AUA.npy
'''
import numpy as np
import sys
from npy import npy2to3

def concatenate(structures_list, nposes, maxat):
    structures = np.zeros((sum(nposes), maxat, 3), dtype=float)
    i = 0
    nat = []
    for ns, s in enumerate(structures_list):
        s_nposes, s_nat, s_ncoor = s.shape
        structures[i : i + s_nposes, : s_nat] = s
        i += s_nposes
        for j in range(s_nposes):
            nat.append(s_nat)
    return np.array(nat), structures

def deconcatenate(structures, nposes, nat):
    structure_list = []
    count = 0
    for p in nposes:
        n = nat[count]
        structure_list.append(structures[count:count+p, :n])
        count += p
    return structure_list

def map_chains(chains, pools, nposes, nfrags):
    mapped_chains = np.zeros((len(chains), len(chains[0])), dtype=int)
    maxpairs = int(len(chains)*0.5*(nfrags-3)*(nfrags-2))
    print("maxpairs: ", maxpairs)
    pairs = np.zeros((maxpairs,2), dtype=np.int32)
    count = 0
    for nc, c in enumerate(chains):
        for ni, i in enumerate(c[:nfrags-3]):
            newi = sum(nposes[:pools[ni]]) + i
            mapped_chains[nc,ni] = newi
            for nj, j in enumerate(c[ni+3:]):
                nj = nj+ni+3
                newj = sum(nposes[:pools[nj]]) + j
                mapped_chains[nc,nj] = newj
                pairs[count] = [newi,newj]
                count += 1
    pairs = np.unique(pairs, axis=0)
    return pairs, mapped_chains

def get_clashes_extra(structures, pairs, threshold, nat, maxat):
    print("############## get_clashes_extra ################")
    print("structures.shape: ", structures.shape)
    print("pairs: ", pairs)
    print("nat.shape: ", nat.shape)
    print("maxat: ", maxat)
    import cffi
    from _get_clashes_extra import ffi
    from _get_clashes_extra.lib import get_clashes_extra
    def npdata(a):
      return a.__array_interface__["data"][0]
    #
    assert pairs.dtype == np.int32, pairs.dtype
    assert structures.dtype == np.double, structures.dtype
    #
    npairs = pairs.shape[0]
    clashes = np.zeros((npairs), dtype=np.int32)
    p_structures = ffi.cast("double *", npdata(structures) )
    p_pairs = ffi.cast("Pair *", npdata(pairs) )
    p_nat = ffi.cast("int *", npdata(nat) )
    p_clashes = ffi.cast("int *", npdata(clashes) )
    n = get_clashes_extra(p_structures, p_pairs, npairs, p_nat, maxat, threshold**2, p_clashes)
    print("%i clashing pairs of poses"%n)
    return clashes[:n]

chains = np.array([ [int(i) for i in l.split()[1:]] for l in open(sys.argv[1]).readlines()] )
nfrags = chains.shape[1]
nchains = len(chains)
cutoff = float(sys.argv[2])
pools = [ int(i) for i in sys.argv[3].split()] # "0 0 0 0" for UUUUUU (4 frags)
                                               # "0 1 0 1" for UAUAUA
assert nfrags > 3 and len(pools) == nfrags
npools = max(pools) + 1
structures_list = [ npy2to3(np.load(i)) for i in sys.argv[4: npools+4]]

#concatenate the motif.npy arrays into one global array of shape
#(total nb of different poses for all motifs, maximal nb of atoms per pose)
maxat = max([ s.shape[1] for s in structures_list])
nposes = [s.shape[0] for s in structures_list]
nat, structures = concatenate(structures_list, nposes, maxat)

# map the poses from motif.npy to the global array of poses
# get the list of pairs
pairs, mapped_chains = map_chains(chains, pools, nposes, nfrags)
print("mapped_chains: ", mapped_chains)

#list all non-redundant clashing pairs of poses
clashing_pairs_indices = get_clashes_extra(structures, pairs, cutoff, nat, maxat)

clashing_pairs = set( [(i,j) for [i,j] in pairs[clashing_pairs_indices]] )
print("clashing_pairs", clashing_pairs)
#print("chains: ", chains)
#print("mapped_chains: ", mapped_chains)

#list clashing chains
clashing_chain_indices = []
for nc, c in enumerate(mapped_chains):
#    print(nc, c)
    clash = 0
    for ni, i in enumerate(c[:nfrags-3]):
#        print("ni,i: ", ni, i)
        for nj, j in enumerate(c[ni+3:]):
#            print("nj,j: ", nj, j)
#            print("i, j:", (i, j))
            if (i, j) in clashing_pairs:
                clashing_chain_indices.append(nc)
                clash = 1
                break
        if clash:
            break

#print(len(clashing_chain_indices))
for clashing in clashing_chain_indices:
    print(clashing)

#np.save(sys.argv[-1], clashes)
