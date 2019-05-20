#!/usr/bin/env python3

import sys
import numpy as np

l1 = [ [int(i) for i in l.split()] for l in open(sys.argv[1]).readlines()]
l2 = [ int(l.split()[0]) for l in open(sys.argv[2]).readlines()]
n2=len(l2)
l2 = set(l2)

print(n2)
for nl, l in enumerate(l1):
    n = len([i for i in l if i in l2])
    print("frag %i: %i of the %i corrects are in tot %i"%(nl+1,n,len(l),n2))
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/count_list1_in_list2.py
