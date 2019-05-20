#!/usr/bin/env python3

#python3 $SCRIPTS/select-dat-perrank.py $motif.dat --score $motif.score \
# --percent 50 --outpscore $tmp/$motif-pc.score > $tmp/$motif-pc.dat

import sys, os, argparse
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc
'''
usage: select-dat-perrank.py <dat file> <rank cutoff> [--percent]
write the top-ranked poses (dat file) from an unsorted input.dat
'''
########################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('dat')
parser.add_argument('--rank', help="number of structures to select", type=float)
#parser.add_argument('--list', help="file containing the list of indices of structures to select")
#parser.add_argument('--index', help="indices of structure to select")
parser.add_argument('--percent', help="percentage of structures to select", type=float)
parser.add_argument('--score', help="file.score", type=str)
parser.add_argument('--outpscore', help="newfile.score", type=str)
args = parser.parse_args()
########################
import itertools

def read_next_struc(lines, firstline):

    assert int(firstline[1:]) == 1
    mode = 1
    ret0,ret1 = [],[]
    lenstruc = 1

    for l in lines:
        l = l.rstrip("\n")
        if mode == 2 and l[0] == "#":
            mode = 0
            yield ret0,ret1
        if mode == 0:
            assert int(l[1:]) == lenstruc + 1
            mode = 1
            ret0,ret1 = [],[]
            lenstruc += 1
            continue
        if mode == 1:
            if l[:2] == "##":
                ret0.append(l)
            else:
                mode = 2
        if mode == 2:
            ret1.append(l)
    if len(ret0) or len(ret1):
        yield ret0,ret1

def read_struc(fil):
    lines = open(fil)
    header = []
    centeredlen = 0
    firstline = None
    for lnr, l in enumerate(lines):
        l = l.rstrip("\n")
        if centeredlen < 2:
            if l.startswith("##"): continue
            header.append(l)
            if l.startswith("#centered"): centeredlen += 1
            continue
        firstline = l
        break
    if firstline is None:
        raise ValueError("Cannot find structures in file %s" % fil)
    return header, read_next_struc(lines,firstline)

def check(l1, cutoff):
    for ll in l1:
        if ll.startswith("## Energy:"):
            ee = ll[10:].strip()
            if ee.startswith("nan") or float(ee) > cutoff :
                return False
    return True

scores = []
if args.score is None:
    header,structures = read_struc(args.dat)
    structures = list(structures)
    for l in open(args.dat):
        if l.startswith("## Energy:"):
            ee = l[10:].strip()
            if ee.startswith("nan"): ee = 10000
            scores.append(float(ee))
else:
    for l in open(args.score,'r'):
        if l[1:7] == "Energy":
            ee = l.split()[1]
            if ee.startswith("nan"): ee = 10000
            scores.append(float(ee))

sorted_scores = sorted(scores)
if args.rank is not None:
    rank = int(args.rank)
elif args.percent is not None:
    print("selecting %i percent"%args.percent,file=sys.stderr)
    rank = round(args.percent * len(sorted_scores)/100)
    print(rank, file=sys.stderr)

cutoff = sorted_scores[rank-1]
print(cutoff, file=sys.stderr)

sorted_scores = []

if args.score is None:
    scores = []

header, structures = read_struc(args.dat)
for l in header:
    print(l)

count=1
if args.score is None:
    for l1,l2 in structures:
        if check(l1, cutoff):
            print("#%i"%count)
            for l in l1 + l2:
                print(l)
            count+=1
else:
    for ns,(l1,l2) in enumerate(structures):
        s = scores[ns]
        if s <= cutoff:
            print("#%i"%count)
            for l in l1 + l2:
                print(l)
            count+=1

if args.outpscore is not None:
    outp = open(args.outpscore, 'w')
    for s in scores:
        if s <= cutoff:
            print(" Energy: %.3f"%s, file=outp)
    outp.close()
