#!/usr/bin/env python3
import sys
import json, argparse
import numpy as np

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('connections')
parser.add_argument('--nposes', help="for prop per pose, at any frag (homo paradigm)", type=int)
parser.add_argument('--firstfrag', help="for prop per frag and per pose", type=int)
args = parser.parse_args()
############

inp = sys.argv[1]
nposes = args.nposes
npz = np.load(inp)

nfrags = npz['nfrags']
max_rmsd = npz['max_rmsd']

#forward
interactions = [npz["interactions-%d" % n] for n in range(nfrags-1)] #count from zero

fwd = [] #fwd for frag 1 - nfrag
weights = None
for n in range(nfrags-1):
    inter = interactions[n]
    assert inter.min() >= 0, inter.min()
    if n > 0:
        weights = prev_count[inter[:, 0]]
    if n < nfrags - 2:
        next_inter = interactions[n+1]
        maxbin = next_inter[:,0].max()
    else:
        maxbin = interactions[n][:,1].max()
    count = np.bincount(inter[:,1], minlength=maxbin+1, weights=weights).astype(int)
    print("fwd", n+1, count.sum(), file=sys.stderr)
    fwd.append(count)
    prev_count = count

bwd = [] #bwd for frag (nfrag-1) - 0
weights = None
for n in range(nfrags-1):
    inter = interactions[nfrags-n-2]
    assert inter.min() >= 0, inter.min()
    if n > 0:
        weights = prev_count[inter[:, 1]]
    if n < nfrags - 2:
        next_inter = interactions[nfrags-n-3]
        maxbin = next_inter[:,1].max()
    else:
        maxbin = interactions[n][:,0].max()
    count = np.bincount(inter[:,0], minlength=maxbin+1, weights=weights).astype(int)
    print("bwd", n, count.sum(), file=sys.stderr)
    bwd.append(count)
    prev_count = count

if args.nposes is not None:
    propstot = np.zeros(args.nposes,dtype=int)
for n in range(nfrags):
    if n == 0:
        props = bwd[-1]
    elif n == nfrags - 1:
        props = fwd[-1]
    else:
        b,f = bwd[-(n+1)], fwd[n-1]
        props = np.ones(min(len(b), len(f)),dtype=int)
        props *= f[:len(props)]
        props *= b[:len(props)]
    if args.firstfrag is not None:
        print(args.firstfrag + n, props.sum(), file=sys.stderr)
        for pnr, p in enumerate(props):
            if not p: continue
            print(args.firstfrag+n, pnr+1, p)
    else:
        propstot[:len(props)] += props

if args.nposes is not None :
    for ni, i in enumerate(propstot):
        print(ni+1, i)
