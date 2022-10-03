import argparse, itertools
p = argparse.ArgumentParser()
p.add_argument('preatom', help='Pre-linkage atom coordinate file (.npy format)')
p.add_argument('postatom', help='Post-linkage atom coordinate file (.npy format)')
p.add_argument('--distances1', help='Backbone overlap distance margins',type=float, nargs="+")
p.add_argument('--distances2', help='Base overlap distance margins',type=float, nargs="+")
p.add_argument('--tolerances', help='Overlap energy tolerances',type=float, nargs="+")
p.add_argument('--clusters1', help='Cluster hierarchies for pre-linkage fragment', nargs="+", default=[])
p.add_argument('--clusters2', help='Cluster hierarchies for post-linkage fragment', nargs="+", default=[])
args = p.parse_args()

assert args.distances1
assert len(args.distances1) == len(args.distances2) == len(args.tolerances)  
levels = len(args.distances1)
assert len(args.clusters1)  == len(args.clusters2) == len(args.distances1) - 1

import sys
import numpy  

oriclusters = [[],[]]

def read_clustfile(clustfile):
  clust = []
  for l in open(clustfile):
    ll = l.split()[3:]
    clust.append([int(v) for v in ll])
  return clust  

for fragnr, clustfiles in enumerate((args.clusters1, args.clusters2)):
  for clustfile in clustfiles:
    clust = read_clustfile(clustfile)
    oriclusters[fragnr].insert(0, clust)
  
bigrange=range(1,100000000)  
clusters = [[],[]]  
coors = [[],[]]
def build_cluster_coor(coor0, fragnr, index, clusnr):  
  if index is None:
    if len(oriclusters[fragnr]):    
      ori = oriclusters[fragnr][0]
      for cnr in range(len(ori)):
        build_cluster_coor(coor0, fragnr, 0, cnr)
    else:
      oriclusters[fragnr].append(bigrange)
      coors[fragnr][0] = coor0
    return
  
  ori = oriclusters[fragnr][index]
  clus = clusters[fragnr][index]
  coor = coors[fragnr][index]
  nclus = len(clus)-1
  ncoor = clus[-1]
  coor2 = coors[fragnr][index+1]
  if index < levels - 2:
    for c in ori[clusnr]:
      build_cluster_coor(coor0, fragnr, index+1, c-1)    
  else:
    for cnr, c in enumerate(ori[clusnr]):
      coor2[ncoor+cnr] = coor0[c-1]      
  clus.append(ncoor + len(ori[clusnr]))
  coor[nclus] = coor2[ncoor]
    
for fragnr, atomf in enumerate((args.preatom, args.postatom)):    
  coor = numpy.load(atomf)
  natoms = coor.shape[1]/3
  coor = coor.reshape(coor.shape[0],natoms,3)
     
  for index in range(levels-1):
    a = numpy.zeros(shape=(len(oriclusters[fragnr][index]),natoms,3))
    coors[fragnr].append(a)
  a = numpy.zeros(shape=coor.shape)  
  coors[fragnr].append(a)
  for index in range(levels):
    clusters[fragnr].append([0])
  build_cluster_coor(coor, fragnr, None, None)
 
assert coors[0][0].shape[1] == coors[1][0].shape[1], (args.preatom, coors[0][0].shape[1], args.postatom, coors[1][0].shape[1])

tolerances = args.tolerances
margins = []
for d1, d2 in zip(args.distances1, args.distances2):
  margin = []
  for k in 1,2: #2 backbone atoms, the rest sidechains
    margin.append(d1)
    margin.append(d1)
    for kk in range(2, natoms/2):
      margin.append(d2)
  margin = numpy.array(margin)
  margins.append(margin) 
 
#for fragnr in 0,1:
#  for cnr in range(len(coors[fragnr])):
#    print >> sys.stderr, fragnr+1, cnr+1, coors[fragnr][cnr].shape


def combinatoric(index, candlist1, candlist2, oricandlist1, oricandlist2):  
  margin = margins[index]
  tolerance = tolerances[index]
  candcoor1 = coors[0][index]
  candcoor2 = coors[1][index] 
  if index < maxindex:
    clust1 = clusters[0][index]
    clust2 = clusters[1][index]
    oriclust1 = oriclusters[0][index]
    oriclust2 = oriclusters[1][index]    
  if index > 0:
    candcoor2 = candcoor2[candlist2]
  else:
    candlist1 = list(range(len(candcoor1)))
    candlist2 = list(range(len(candcoor2)))
    oricandlist1 = list(range(1,len(candcoor1)+1))
    oricandlist2 = list(range(1,len(candcoor2)+1))
  for cand1nr, oricand1nr in zip(candlist1, oricandlist1):
    dif = candcoor2 - candcoor1[cand1nr]
    dis = numpy.linalg.norm(dif,axis=2)
    viol = (dis-margin).clip(min=0)
    e = (viol*viol*100).sum(axis=1)
    match = numpy.where(e<tolerance)[0]    
    if not len(match): continue    
    if index == maxindex:
      for cand2nr in match:     
        print "Energy:", e[cand2nr], oricand1nr, oricandlist2[cand2nr]
    else:    
      candsublist1 = list(range(clust1[cand1nr], clust1[cand1nr+1]))
      iters = [range(clust2[candlist2[c]], clust2[candlist2[c]+1]) for c in match]
      candsublist2 = list(itertools.chain(*iters))
      oricandsublist1 = oriclust1[oricand1nr-1]
      iters = [oriclust2[oricandlist2[c]-1] for c in match]
      oricandsublist2 = list(itertools.chain(*iters))
      assert len(oricandsublist1) == len(candsublist1), (oricandsublist1, candsublist1)
      assert len(oricandsublist2) == len(candsublist2), (oricandsublist2, candsublist2)
        
      combinatoric(index+1, candsublist1, candsublist2, oricandsublist1, oricandsublist2)
    if not index: 
      print >> sys.stderr, cand1nr+1
    
maxindex = levels - 1
combinatoric(0, None, None, None, None)
