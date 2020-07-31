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


header1,structures1 = read_struc(args.dat1)
header2,structures2 = read_struc(args.dat2)

lines1 = [ l2[1] for l1, l2 in structures1 ]
lines2 = [ l2[1] for l1, l2 in structures2 ]

#if no conformers:
#    lines1 = [ int(l.split()[2]) for l in open(args.dat1).readlines() if l.startswith("### SEED")]
#    lines2 = [ int(l.split()[2]) for l in open(args.dat2).readlines() if l.startswith("### SEED")]

set2 = set(lines2)
indices = [ i for i, val in enumerate(lines1) if val in set2]

for i in indices:
    print i+1
