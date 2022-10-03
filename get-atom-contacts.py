#!/usr/bin/env python3

import numpy as np
import sys,os, argparse

############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pdb1', help="1st pdb")
parser.add_argument('pdb2', help="2nd pdb")
parser.add_argument("cut",help="max contact distance", type=float)
args = parser.parse_args()
############
'''
ATOM      1  GP1  RG     1      42.131  58.379 115.046   32   0.000 0 1.00
'''
pdb1 = [ l for l in open(args.pdb1).readlines() if l.startswith("ATOM") ]
coord1 = [ [float(l[30:38]),float(l[38:46]),float(l[46:54])] for l in pdb1 ]
atname1 = [ l[13:17].strip() for l in pdb1 ]
resname1 = [ l[17:21].strip() for l in pdb1 ]
resid1 = [ int(l[21:27]) for l in pdb1 ]
Nat1 = len(pdb1)

pdb2 = [ l for l in open(args.pdb2).readlines() if l.startswith("ATOM") ]
coord2 = [ [float(l[30:38]),float(l[38:46]),float(l[46:54])] for l in pdb2 ]
atname2 = [ l[13:16].strip() for l in pdb2 ]
resname2 = [ l[17:21].strip() for l in pdb2 ]
resid2 = [ int(l[21:27]) for l in pdb2 ]
Nat2 = len(pdb2)

cut = args.cut

for i in range(Nat1):
    for j in range(Nat2):
        D = sum( [(coord1[i][a]-coord2[j][a])**2 for a in range(3) ] )**0.5
        if D < cut :
            print("%.3f\t|  %i\t%s\t%s\t%i\t |  %i\t%s\t%s\t%i"%(D, i, atname1[i], resname1[i], resid1[i], j, atname2[j], resname2[j], resid2[j]), file=sys.stderr)
#        pairing.append((i, j, ))
