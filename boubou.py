#!/usr/bin/env python 

import numpy as np
import sys,os, argparse, time
from scipy.spatial.distance import cdist
attract = os.environ["ATTRACTDIR"]
############
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('pdb1', help="np array")
parser.add_argument('pdb2', help="np array")
parser.add_argument("--fit",help="fit on 1st structure", action="store_true")
args = parser.parse_args()
############

def pdbparse(pdbfile):
    pdb = [ l for l in open(pdbfile).readlines() if l.startswith("ATOM") ]
    coord = np.array([ [float(l[30:38]),float(l[38:46]),float(l[46:54])] for l in pdb ])
    beadtype =  np.array([ int(l[57:59]) for l in pdb ])
    Nat = len(pdb)
    return pdb, coord, beadtype, Nat
    
pdb2, coord2, type2, Nat2 = pdbparse(args.pdb2)
pdb1, coord1, type1, Nat1 = pdbparse(args.pdb1)

def mapp(atindex1, atindex2):
    t1, t2 = type1[atindex1], type2[atindex2]
    if t1 == 99 or t2 == 99:
        return np.nan
    else:
        return rmin[ t1-1, t2-1 ]

D = cdist(coord1, coord2)

print D.min()
