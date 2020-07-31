#!/usr/bin/env python2
import sys, os, argparse
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc

########################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat1')
parser.add_argument('dat2')
args = parser.parse_args()
########################

seed1 = [ l.split()[2] for l in open(args.dat1).readlines() if l.startswith("### SEED")]
seed2 = [ l.split()[2] for l in open(args.dat2).readlines() if l.startswith("### SEED")]

set2 = set(seed2)
res = [i for i, val in enumerate(seed1) if val in set2]

for r in res:
    print r
