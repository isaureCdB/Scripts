#!/usr/bin/env python3

import sys, os, argparse
import numpy as np

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('chains', type=str)
parser.add_argument('nfrag', type=int)
parser.add_argument('lrmsd', nargs='+', help="list of frag lrmsd")
parser.add_argument('--average', action="store_true")
args = parser.parse_args()
############

nfrag = args.nfrag
cc =  [ l for l in open(args.chains).readlines()[1:]]
chains = [ [int(i)-1 for i in l.split()[2:2+nfrag]] for l in cc]
print(args.lrmsd)
lrmsds = [ [float(l.split()[-1]) for l in open(f).readlines()] for f in args.lrmsd]

if args.average:
    for c in chains:
        rms = []
        for np, p in enumerate(c):
            rms.append(lrmsds[np][p])
        a = [sum(rms**2)/nfrag]**0.5
        print(a)

else:
    for c in chains:
        for np, p in enumerate(c):
            print(lrmsds[np][p], end=" ")
        print("")
