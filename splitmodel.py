#!/usr/bin/python3

import sys, argparse
########################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('multipdb')
parser.add_argument('template', help="pattern for output files")
parser.add_argument('--list', help="template is a list of output files", action="store_true")
args = parser.parse_args()
########################
f = args.multipdb
template = args.template
nstruct = 999999999
if args.list:
    template = [ l.split()[0] for l in open(template) ]
    nstruct = len(template)

count = 0
for l in open(f):
    l = l.rstrip("\n")
    if l.startswith("MODEL"):
        if count > 0: ff.close()
        count += 1
        target = template + str(count-1)
        print(target)
        ff = open(target, "w")
        continue
    if not l.startswith("ATOM"): continue
    print(l, file=ff)
