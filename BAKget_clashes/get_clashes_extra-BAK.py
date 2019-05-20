'''
detect which chains of poses have clashes for any pair of fragments (f,f+i) with i>2
usage: python get_clashes_extra.py chains.txt <cutoff in A> <mapping> <motif1.npy> <motif2.npy>
<mapping> : string mapping fragments to motifs.
            ex: for a UAUAUA sequence, use "0 1 0 1" with UAU.npy AUA.npy
'''
import numpy as np
import sys
from npy import npy2to3
from math import factorial as fact

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

def map_chains(chains, pools, nposes, nfrags):
    mapped_chains = np.zeros((len(chains), len(chains[0])), dtype=int)
    maxpairs = len(chains)*(nfrags - 3)
    pairs = np.zeros((maxpairs,2), dtype=int)
    count = 0
    for nc, c in enumerate(chains):
        for ni, i in enumerate(c[:nfrags-3]):
            for nj, j in enumerate(c[i+3:]):
                mapped_chains[nc,ni] = sum(nposes[:pools[ni]]) + i
                pairs[count] = [i,j]
                count += 1
    return pair, mapped_chains

def get_pairs(nfrags, nposes, mapped_chains):
    pairs = np.zeros((nposes*nposes,2), dtype=int)
    for i in range(nfrags-3):
        for j in range(i+3,nfrags):
            key = (pools[i], pools[j])
            if key not in pair_pools.keys():
                pair_pools[key] = np.zeros((0,2), dtype=int)
            p = pair_pools[key]
            new_p = mapped_chains[:,[i,j]]
            print("shape p: ", p.shape)
            print("shape new_p:", new_p.shape)
            pair_pools[key] = np.unique(np.concatenate((p,new_p), axis=0), axis=0)
    return pair_pools

def get_clashes_extra(structures, pairs, threshold, nat, maxat):
    import cffi
    from _get_clashes_extra import ffi
    from _get_clashes_extra.lib import get_clashes_extra
    def npdata(a):
      return a.__array_interface__["data"][0]
    npairs = pairs.shape[0]
    clashes = np.zeros((npairs), dtype=int)
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
#print("structures.shape: ", structures.shape)
#print("pairs.shape: ", pairs.shape)
#print("pairs: ", pairs)
#print("nat.shape: ", nat.shape)
#print("maxat: ", maxat)
clashing_pairs_indices = get_clashes_extra(structures, pairs, cutoff, nat, maxat)
print("clashing_pairs_indices: ",clashing_pairs_indices )

clashing_pairs = set(pairs[clashing_pairs_indices])

#list clashing chains
clashing_chain_indices = []
for nc, c in enumerate(mapped_chains):
    clash = 0
    for ni, i in enumerate(c[:nfrags-3]):
        for nj, j in enumerate(c[i+3:]):
            if [i, j] in clashing_pairs:
                clashing_chain_indices.append(nc)
                clash = 1
                break
        if clash:
            break

for clashing in clashing_chain_indices:
    print(clashing)

#np.save(sys.argv[-1], clashes)
