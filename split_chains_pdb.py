#!/usr/bin/env python3

import sys

def pp(l):
    global files
    for c in files:
        print(l[:-1], file = files[c])

inp = sys.argv[1]
name = inp.split(".pdb")[0]
files = {}
chain = None
for l in open(inp):
    if l.startswith("TER") or l.startswith("ENDMDL") or l.startswith("MODEL"):
        pp(l)
        continue
    if not l.startswith("ATOM"): continue
    c = l[21]
    if c not in files:
        files[c] = open("%s-%s.pdb"%(name,c),"w")
    print(l[:-1], file = files[c])

for c in files:
    files[c].close()
