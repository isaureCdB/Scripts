list = "UUU-e6-8frag-1.3_connected-spacing5.list"
npz1 = "UUU-e6-8frag-1.3.npz"
npz2 = "UUU-e6-8frag-1.3_connected-spacing5.npz"
##########
list = "x-6frag-5A_connected-spacing2.list"
npz1 = "x-6frag-5A.npz"
npz2 = "x-6frag-5A_connected-spacing2.npz"



npz=np.load(npz1)

interactions = [npz["interactions-%i"%i] for i in range(nfrags-1)]

nfrags = npz["nfrags"]

connectednpz=np.load(npz2)

map1=[int(l.split()[0])-1 for l in open(list).readlines()]

connected=[connectednpz[str(i)] for i in range(len(map1))]


for cnr, c in enumerate(connected):
    for i in c:
       assert cnr in connected[i], (cnr, i)

chainmapped = [ [mapcliques[i-1] for i in c] for c in chains ]
for nc, c in enumerate(chainmapped):
    for i in range(8):
        for ii in range(i+1, min(8, i+5)):
           assert c[i] != c[ii], (nc, c)
clashing=[]
for nc, c in enumerate(chainmapped):
    for i in range(3):
        for ii in range(i+6, 8):
           if c[i] == c[ii]:
               clashing.append(nc)

chains=[ [int(i) for i in l.split()[2:]] for l in open("UUU-e6-8frag-1.3.chains").readlines()[1:]]
cliques=[ [int(i) for i in l.split()[3:]] for l in open("../color_coding/UUU-e6-8frag-1.3_connected-spacing5.cliques-6A").readlines()]
mapcliques={}
for clnr, cl in enumerate(cliques):
    for i in cl:
        mapcliques[i]=clnr

chainmapped = [ [mapcliques[i] for i in c] for c in chains[:5] ]
len(set([tuple(i) for i in chainmapped]))
import numpy as np
cm = np.array(chainmapped)
cm.shape
np.unique(cm[:,4], return_index=True)
len(cm)
np.unique(cm[:,4], return_counts=True)[1].sum()
np.unique(cm[:,4], return_counts=True)
len(set([tuple(i) for i in chainmapped]))
set([tuple(i) for i in chainmapped])
chainset = set([tuple(i) for i in chainmapped])
[c for c in chainset if len(set(c)) < 8]

%history
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/check-clique.py
