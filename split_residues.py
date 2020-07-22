#!/usr/bin/env python3

import sys
pdb = open(sys.argv[1])
name = sys.argv[1].split(".pdb")[0]

r = None
for l in pdb.readlines():
    if not (l.startswith("ATOM") or l.startswith("HETATM")):
        continue
    if str(l[21:27]).strip() != r:
        if r is not None:
            outp.close()
        r = str(l[21:27]).strip()
        outp = open("%s-%s.pdb"%(name,r), "w")
        print("%s-%s.pdb"%(name,r))
    outp.write(l)

outp.close()

#ATOM     59  H8  DA      1     -11.393   9.346  47.649  0.1877 1.3590
