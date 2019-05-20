#!/usr/bin/env python3

import sys

header = sys.argv[1]
coordinates = sys.argv[2]

ene = []
if len(sys.argv)==4:
    ene = [float(l) for l in open(sys.argv[3])]

for l in open(header, 'r'):
    print(l[:-1])

i=1
for l in open(coordinates, 'r'):
    if l.startswith('#'):
        continue
    print("#%i"%i)
    if len(ene) > 0 :
        print('# Energy: %.3f'%ene[i-1])
    print(" 0 0 0 0 0 0")
    print(l[:-1])
    i+=1
