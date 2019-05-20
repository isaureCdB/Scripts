#!/usr/bin/env python3

import sys
pdb = open(sys.argv[1])
name = sys.argv[1].split(".pdb")[0]

j = 1
outp = open("%s-%i.pdb"%(name,j), "w")
for l in pdb.readlines():
    if l.startswith("TER"):
        outp.close()
        j+=1
        outp = open("%s-%i.pdb"%(name,j),"w")
    elif l.startswith("ATOM") or l.startswith("HETATM"):
        outp.write(l)
outp.close()
