# Credit: Josh Hemann

import numpy as np, sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

n_groups = 12

data1 = [float(l.split()[0]) for l in open(sys.argv[1]).readlines()]

data2 = [float(l.split()[0]) for l in open(sys.argv[2]).readlines()]

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
#error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, data1, bar_width,
                #alpha=opacity,
                color='limegreen',
                #error_kw=error_config,
                label='ATTRACT')

rects2 = ax.bar(index + bar_width, data2, bar_width,
                #alpha=opacity,
                color='royalblue',
                #error_kw=error_config,
                label='deepATTRACT')
plt.yscale('log')
ax.set_xlabel('fragment index')
ax.set_ylabel('RMSD')
ax.set_title('Best rmsd per fragment (angstroem)')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels([str(i) for i in range(1, len(data1)+1)])
ax.legend()

fig.tight_layout()
fig.savefig('barchart.png', bbox_inches='tight')

plt.show()
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/barchart_demo.py
