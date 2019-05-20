#!/usr/bin/env python
import sys
frag = [ l for l in open(sys.argv[1]).readlines()]
P = [l for l in frag if l[13:16] == "GP1"]
print(P)
coor = [[float(i) for i in [l[29:38],l[38:47],l[47:54]]] for l in P]
#print(coor)
dist1 = (sum([ (coor[0][i]-coor[1][i])**2 for i in range(3) ]))**0.5
#dist2 = (sum([ (coor[1][i]-coor[2][i])**2 for i in range(3) ]))**0.5
#dist3 = (sum([ (coor[2][i]-coor[0][i])**2 for i in range(3) ]))**0.5
print(dist1)
#print("%.2f %.2f %.2f"%(dist1, dist2, dist3))
