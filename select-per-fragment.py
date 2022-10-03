import sys, os, bisect
sys.path.append(os.environ["ATTRACTTOOLS"])
from _read_struc import read_struc

dat = sys.argv[1]
pct = float(sys.argv[2])

# First pass: determine the count of each conformer
count = {}
header, struc = read_struc(dat)
for s1, s2 in struc:
  for l in s1:
    ll = l.split()
    if ll[0] == "##" and ll[1] == "Energy:":
      break
  else:
    raise Exception("Cannot find energies")    
  conf = int(s2[1].split()[0])
  if conf not in count: count[conf] = 0
  count[conf] += 1
  
pctcount = {}
for conf in count:
  pctcount[conf] = int(pct * count[conf] + 0.5)

# Second pass: determine the selected strucs based on energy
strucs = {}
energies = {}
for conf in count:
  strucs[conf] = []
  energies[conf] = []

header, struc = read_struc(dat)
for stnr, s in enumerate(struc):
  s1, s2 = s
  for l in s1:
    ll = l.split()
    if ll[0] == "##" and ll[1] == "Energy:":
      ene = float(ll[2]) 
      break
  else:
    raise Exception("Cannot find energies")    
  
  conf = int(s2[1].split()[0])  
  cst, cene, cpct = strucs[conf], energies[conf], pctcount[conf]
  point = bisect.bisect_right(cene, ene)
  if point > cpct: continue
  cene.insert(point, ene)
  cst.insert(point, stnr)
  if len(cst) > cpct:
    cst.pop()
    cene.pop()
  
selected = set()
for selstrucs in strucs.values():
  selected.update(set(selstrucs))

# Third pass: print the selected structures
header, struc = read_struc(dat)
for h in header: print h
counter = 0
header, struc = read_struc(dat)
for stnr, s in enumerate(struc):
  if stnr not in selected: continue
  s1, s2 = s
  counter += 1
  print "#%d" % counter
  for l in s1: print l
  for l in s2: print l
  