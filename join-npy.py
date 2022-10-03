#!/usr/bin/env python3

import numpy as np
import sys, argparse

#############
parser=argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('npyout', help="output np array")
parser.add_argument('npys', nargs="+", help="input np arrays")
args = parser.parse_args()
##############

npys = [np.load(f) for f in args.npys]

for j in npys:
	print(j.shape)

x = np.concatenate(npys)

np.save(args.npyout, x)
