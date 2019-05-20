#!/usr/bin/env python3

import sys
name=sys.argv[1]

l = [int(l.split()[0]) for l in open(name+"-interface-l.dat")]
r = [int(l.split()[0]) for l in open(name+"-interface-r.dat")]

Nl=len(l)
Nr=len(r)

print("A_actpass %i "%Nr, end="")
for i in r:
    print(i, end=" ")
print("")

print("B_actpass %i "%Nl, end="")
for i in l:
    print(i, end=" ")
print("")

for i in l:
    print("A_%i 1 %i"%(i, i))
for i in r:
    print("B_%i 1 %i"%(i, i))

print("")

for i in l:
    print("A_%i B_actpass 2 3.0 1.0 3.0 0.5"%i)
for i in r:
    print("B_%i A_actpass 2 3.0 1.0 3.0 0.5"%i)
