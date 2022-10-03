import numpy as np

def frac(a,l):
    print((lrmsd10[a]<l).sum()/len(lrmsd10[a])*100)

def enrich5(a):
    frac(a,5)
    print((lrmsd10[a]<5).sum()/len(lrmsd10[a]) / frac5_ori)

def enrich4(a):
    frac(a,4)
    print((lrmsd10[a]<4).sum()/len(lrmsd10[a]) / frac4_ori)

# dist of base to phenylalanine cycle
def dist_phe_base(ph, rna, at1, at2):
    base = rna[:, at1:at2, :]
    d = base - ph[None,None,:]
    phs = (np.sum(d**2, axis=(1,2))/3)**0.5
    return phs

lrmsd10 = np.loadtxt("rna-10mer.rmsd")[:,1]
frac4_ori = (lrmsd10<4).sum()/len(lrmsd10)
frac5_ori = (lrmsd10<5).sum()/len(lrmsd10)

coor = np.load("rna.npy")
s = coor.shape
rna = coor.reshape((-1,int(s[1]/3),3))

#linearity retrains (min dist i - i+3)
mindist = np.load("mindist_nucl_rna.npy")
min = mindist.min(axis=1)

#distance 3' phosphates from Mg ion
mg = np.array([-6.434, 0.395, -16.773])
P1 = (np.sum((rna[:,60]-mg[None,:])**2, axis=1))**0.5
P2 = (np.sum((rna[:,54]-mg[None,:])**2, axis=1))**0.5

#position of phynylalanine 2nd side-chan bead
ph=np.array([13.426,  -3.077,  19.166])
ph1s = dist_phe_base(ph, rna, 3, 6)
ph2s = dist_phe_base(ph, rna, 9, 12)

ph1s4=ph1s<4

enrich5((P1<7)&(min>6)&(ph1s<5) )
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/filter.py
