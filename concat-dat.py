#!/usr/bin/env python2
import sys, os, argparse
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc


########################
parser =argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('datlist', nargs="*")
args = parser.parse_args()
########################

def check(l1, cutoff):
    for ll in l1:
        if ll.startswith("## Energy:"):
            ee = ll[10:].strip()
            if ee.startswith("nan") or float(ee) > cutoff :
                return False
    return True

header = read_struc(args.datlist[0])

structureslist = [ read_struc(dat)[1] for dat in args.datlist]

n = 1
for l in header:
    print(l)
for structures in structureslist:
	for l1,l2 in structures:
		  print('#'+str(n))
		  n+=1
		  for l in l1[1:] + l2:
		      print(l)
