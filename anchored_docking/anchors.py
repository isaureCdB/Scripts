#!/usr/bin/python2.7
import sys, os, string

pdb=open(sys.argv[1],'r').readlines()
anchor=open(sys.argv[2],'r').readlines()
at=int(pdb[-1][7:11])+1
res=int(pdb[-1][22:27])+1

for line in pdb:
  print l


for line in anchor:
  if line.split()[0]!='ATOM':continue
  print "%s%4d%s%4d%s%s%s" % (line[:7], at, line[11:22], res, line[26:57], "99", line[59:-1])
  at+=1
  res+=1


