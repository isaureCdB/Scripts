import pandas as pd
from io import StringIO
from numpy import random
result = [{"x": [0, 100], "y": [0, 100]}]

df = pd.read_csv(StringIO(csv))
#print(df.complex)
#print(df.complex[0] == df.complex[1])
occupied = {}
for complex in df.complex.unique():
    cdf=df[df.complex==complex]
    cdf=cdf[(df.attract_hits>0) |  (cdf.autodock_hits>0)]
    frags = cdf[cdf.columns[1]].tolist()
    for n in range(2, len(df.columns), 2):
        v1, v2 = cdf[cdf.columns[n]], cdf[cdf.columns[n+1]]
        x = v1.tolist()
        y = v2.tolist()
        for nn in range(len(v1)):
            vv1, vv2 = x[nn], y[nn]
            occ = occupied.get((vv1, vv2), 0)
            if occ % 2:
                x[nn] -= point_shift * (occ+1)/2
            else:
                x[nn] += point_shift * occ/2
            occupied[(vv1, vv2)] = occ + 1
        result.append({"x": x, "y": y})
return result
