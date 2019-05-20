# Credit: Josh Hemann

import numpy as np, sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


inf5 = np.array([ 0.31, 0.43, 0.81, 10.3, 2.67, 16.2, 50, 100])
inf4 = np.array([0.047, 0.079, 0.81, 1.68, 2.67, 2.93, 50, 100])
size = np.array([100000, 49579, 371, 1428, 75, 784, 2, 1])
enrich5 = inf5/inf5[0]
enrich4 = inf4/inf4[0]

colors = ['gray', 'magenta', 'cyan', 'yellow', 'b', 'r', 'limegreen', 'black']
fig, ax = plt.subplots()

bar_width = 0.85

#opacity = 0.4
#error_config = {'ecolor': '0.3'}

rects1 = ax.bar(range(8), inf4, bar_width,
                #alpha=opacity,
                color=colors,
                #error_kw=error_config,
                label='ATTRACT',
                hatch='//',
                )


plt.yscale('log')
ax.set_xlabel('fragment index')
ax.set_ylabel('RMSD')
ax.set_title('Best rmsd per fragment (angstroem)')
ax.legend()

ax.bar(range(8), inf5-inf4, bar_width, bottom = inf4, color=colors)

fig.tight_layout()
fig.savefig('barchart.png', bbox_inches='tight')

plt.show()
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/barchart_enrich.py
