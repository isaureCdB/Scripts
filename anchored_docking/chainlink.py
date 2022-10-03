import sys
from math import log

def read_possible(f):
  pos = {}
  for l in open(f).readlines():
    if not len(l.strip()): continue
    ll = l.split()
    assert ll[0] == "Energy:", l
    l1 = int(ll[2])
    l2 = int(ll[3])
    if l1 not in pos: pos[l1] = set()
    pos[l1].add(l2)
  return pos

possible_files = sys.argv[1:]

def propagate_possible(f, candidates):
  propcand = set()
  for l in open(f).xreadlines():
    if not len(l.strip()): continue
    ll = l.split()
    assert ll[0] == "Energy:", l
    l1 = int(ll[2])
    if candidates is not None and l1 not in candidates: 
      continue
    l2 = int(ll[3])
    propcand.add(l2)
  return propcand

def backpropagate_possible(f, candidates1, candidates2):
  propcand = set()
  for l in open(f).xreadlines():
    if not len(l.strip()): continue
    ll = l.split()
    #assert ll[0] == "Energy:", l
    l1 = int(ll[2])
    if candidates1 is not None and l1 not in candidates1: 
      continue
    l2 = int(ll[3])
    if l2 not in candidates2: 
      continue    
    propcand.add(l1)
  return propcand

def propagate_counts(f, candidates1, candidates2, propcount1):
  count2 = 0
  propcount2 = {}
  for cand2 in candidates2: propcount2[cand2] = 0.0
  
  for l in open(f).xreadlines():
    if not len(l.strip()): continue
    ll = l.split()
    #assert ll[0] == "Energy:", l
    l1 = int(ll[2])
    if l1 not in candidates1: 
      continue
    l2 = int(ll[3])
    if l2 not in candidates2:
      continue
    inc = 1.0
    if propcount1: inc = propcount1[l1]
    propcount2[l2] += inc
    count2 += 1
  return count2, propcount2

def backpropagate_counts(f, candidates1, candidates2, propcount2):
  count1 = 0
  propcount1 = {}
  for cand1 in candidates1: propcount1[cand1] = 0.0
  
  for l in open(f).xreadlines():
    if not len(l.strip()): continue
    ll = l.split()
    #assert ll[0] == "Energy:", l
    l1 = int(ll[2])
    if l1 not in candidates1: 
      continue
    l2 = int(ll[3])
    if l2 not in candidates2:
      continue
    inc = 1.0
    if propcount2: inc = propcount2[l2]
    propcount1[l1] += inc
    count1 += 1
  return count1, propcount1


chain = len(possible_files)

#forward propagation
print >> sys.stderr, "forward propagation"
candidates = [None]
for ch in range(chain):
  f = possible_files[ch]
  propcand = propagate_possible(f, candidates[-1])
  print >> sys.stderr, ch+1, len(propcand)
  candidates.append(propcand)
  
#backward propagation
print >> sys.stderr, "backward propagation"
bcandidates = [candidates[-1]]
for ch in range(chain,0,-1):
  f = possible_files[ch-1]
  cand2 = bcandidates[-1]
  cand1 = candidates[ch-1]
  propcand = backpropagate_possible(f, cand1, cand2)
  print >> sys.stderr, ch-1, len(propcand)
  bcandidates.append(propcand)
candidates = list(reversed(bcandidates))

#forward count propagation
print >> sys.stderr, "forward count propagation"
counts=[None]
propcounts = [None]
for ch in range(chain):
  f = possible_files[ch]
  cand1 = candidates[ch]
  cand2 = candidates[ch+1]
  vcounts, pcounts = propagate_counts(f, cand1, cand2, propcounts[-1])
  print >> sys.stderr, ch+1, len(cand2), sum(pcounts.values())
  counts.append(vcounts)
  propcounts.append(pcounts)

#backward count propagation
print >> sys.stderr, "backward count propagation"
bpropcounts = [None]
for ch in range(chain):
  ch2 = chain-ch-1
  f = possible_files[ch2]
  cand1 = candidates[ch2]
  cand2 = candidates[ch2+1]
  vcounts, pcounts = backpropagate_counts(f, cand1, cand2, bpropcounts[-1])
  print >> sys.stderr, ch2+1, len(cand2), sum(pcounts.values())
  bpropcounts.append(pcounts)

#totcount propagation
totcountsum = sum(propcounts[-1].values())
assert totcountsum == sum(bpropcounts[-1].values()), (totcountsum, sum(bpropcounts[-1].values()))
bpropcounts.reverse()

print >> sys.stderr, "Possible chains:", totcountsum
for ch in range(chain+1):
  c = propcounts[ch]
  bc = bpropcounts[ch]
  if c is None:
    c = {}
    for k in bc: c[k] = 1
  if bc is None:
    bc = {}
    for k in c: bc[k] = 1
  totcount = {}
  for k in c:
    totcount = c[k] * bc[k]
    score = totcount/totcountsum
    if score >= 0.0001:
      print "%.3f %d %d" % (log(score), k, ch+1)
      
    
    
