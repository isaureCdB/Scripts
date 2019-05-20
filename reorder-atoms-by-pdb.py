#!/usr/bin/python2.7

import sys
import os

def run(command):
  sys.stdout.flush()
  os.system(command)
  
f = open(sys.argv[1],'r')
ref = open(sys.argv[2],'r')

resset = set([])
Order = {}
exresid = ""
exres = ""
atoms = []
for l in ref:
  if l[:4]!="ATOM":continue
  res = l[17:20]
  resid = l[22:26]
  if resid != exresid:
    if exres not in resset:
      Order[exres] = atoms
      resset.add(exres)
    atoms = [] 
  atoms.append(l[13:17]) 
  exresid = resid  
  exres = res  

hi = False
for aa in ['HIS','HIE'] :
  if aa in Order.keys():
    hist = aa
    hi = True

if hi:
  for aa in ['HIS','HIE'] :
    Order[aa] = Order[hist]

def reorder(res):
#    print >> sys.stderr, res
    aa = res[0][17:20]
    atoms = [x[13:17] for x in res ]
#    print >> sys.stderr, aa, Order[aa]
    res.sort(key = lambda s:Order[aa].index(s[13:17]))
    for k in res: print k,
    res = []
    return(res)

res = []
for l in f:
  if l.split()[0]!='ATOM':
    if len(res) > 1: res = reorder(res)
    print l,
    continue
  resid = l[22:26]
  if len(res) < 1:
    res.append(l)
    continue 
  if resid != res[-1][22:26]:
    res = reorder(res)
  res.append(l)

if len(res) > 1: res = reorder(res)  

f.close()
ref.close()
