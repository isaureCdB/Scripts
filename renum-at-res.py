#!/usr/bin/python2.7
import sys, os, string

pdb = open(sys.argv[1],'r').readlines()

previouschain="z"
previous=10000
at = 0
res = 0
beg = True

for line in pdb:
  p = line.split()
  if p[0]=='ENDMDL' or p[0]=='END' or p[0]=='MODEL':
    print line[:-1]
    at = 0
    res = 0
    beg = True
    continue
  if p[0]=='TER':
    res = 0
    beg = True
    print line[:-1]
    previous = -100
    continue
  if p[0]!='ATOM' or line[16]=="B": # BARG, BVAL ...
    continue
#    raise ValueError("non recognised line %s" %p)
  at+=1
  resnum = int(line[22:26])
#  print(resnum)
  chain = line[21]
  if p[2]=='P' or p[2]=='N' or chain != previouschain or resnum != previous:
    res += 1
    if resnum != previous+1 and not beg:
      print 'TER'
  beg=False
  previous = resnum
  previouschain = chain
  print "%s%5d%s%4d%s" % (line[:6], at, line[11:22], res, line[26:-1])
