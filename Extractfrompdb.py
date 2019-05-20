#!/usr/bin/python2.7
import sys
import os
Rank=[int(r) for r in sys.argv[2:]]
f=open(sys.argv[1]+'.pdb','r')
g=[open(sys.argv[1]+'-rk'+str(r)+'.pdb','w') for r in sys.argv[2:]]
p=f.readlines()
P=p
r=0
struct=1
i=0
while i in range(len(P)) and r in range(len(Rank)):
	if struct==Rank[0]:g[Rank[r]].write(P[i])
	if P[i].split()[0]=='END' or P[i].split()[0]=='ENDMDL' :
		if struct==Rank[0]:
			g[Rank[r]].write(P[i])
			g[Rank[r]].close()
			r+=1
		struct+=1
	i+=1

g.close()
