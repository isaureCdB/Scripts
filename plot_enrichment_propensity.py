#!/usr/bin/env python3
import numpy as np, sys
selection = sys.argv[1]
propensities = sys.argv[2]
rmsdfile = sys.argv[3]

sel = np.loadtxt(selection, dtype=int)[:,0]-1
prop = np.loadtxt(propensities, dtype=int)[sel,1]
rmsd_rank = np.loadtxt(rmsdfile, dtype=float)[sel,1]
propranks = np.argsort(-prop, axis=0)
rmsd_prop = rmsd_rank[propranks]
good_prop = rmsd_prop<5.05
good_rank = rmsd_rank<5.05
prop_plot = np.cumsum(good_prop)
rank_plot = np.cumsum(good_rank)
from matplotlib import pyplot as plt
plt.plot(prop_plot/good_rank.sum(), "red")
plt.plot(rank_plot/good_rank.sum(), "blue")
plt.plot([0,len(sel)],[0,1], "black")
plt.show()
