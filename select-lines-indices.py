#!/usr/bin/env python3
import sys, argparse

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('data')
parser.add_argument('selection')
parser.add_argument("--noorder",help="order along data file", action="store_true")
parser.add_argument("--reverse",help="take absent lines", action="store_true")
parser.add_argument("--indices",help="print lines indices instead of line", action="store_true")
args = parser.parse_args()
#######################

data = open(args.data).readlines()
selection = open(args.selection).readlines()

def pprint(i, l):
    if args.indices:
        print(i+1)
    else:
        print(l)

if args.reverse:
    sset = set(s)
    for nd, d in enumerate(data):
        if d not in sset:
            if args.indices:
                pprint(nd, d)
else:
    if args.noorder:
        sset = set(s)
        for nd, d in enumerate(data):
            if d in sset:
                pprint(nd, d)
    else:
        for s in selection:
            for nd, d in enumerate(data):
                if d = s:
                    pprint(nd, d)
