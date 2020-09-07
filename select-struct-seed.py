#!/usr/bin/env python2
import sys, argparse
from _read_struc import read_struc

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat')
parser.add_argument('seeds',help="list of seeds to select")
parser.add_argument("--dataorder",help="keep order from dat file", action="store_true")
args = parser.parse_args()
#######################

def write_structure(struct, n):
    l1,l2 = struct
    print "#"+str(n)
    try:
        for l in l1: print l
        for l in l2: print l
    except IOError:
        sys.exit()

header,structures = read_struc(args.dat)
seeds = [l.split()[0] for l in open(args.seeds).readlines()]
selected_set = set(seeds)

for h in header: print h

selstruc = {}
n = 0
for s in structures:
    l1,l2 = s
    seed = [l.split()[2] for l in l1 if l.startswith("### SEED")][0]
    if n == 0:
        print >> sys.stderr, seed
    if seed not in selected_set: continue
    n += 1
    if args.dataorder:
        write_structure(s, n)
        continue
    selstruc[seed] = s

print >> sys.stderr, seeds[0]


if not args.dataorder:
    for ns, seed in enumerate(seeds):
        write_structure(selstruc[seed], ns)
