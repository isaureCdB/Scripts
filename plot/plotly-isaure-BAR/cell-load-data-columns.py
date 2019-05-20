import pandas as pd
from io import StringIO
from numpy import random
#result = [{"x": [0, 100], "y": [0, 100]}]

print("OK")
df = pd.read_csv(StringIO(csv))
#x = list(df.columns)[2:4]
x = []
cutoff3 = []
cutoff53 = []
best = []
for row in df.index:
    r = df.ix[row].tolist()
    x.append(r[0]+r[1])
    cutoff3.append(r[2])
    cutoff53.append(r[3]-r[2])
    best.append(r[4]*10)
return [{"x": x, "y": cutoff3, "name": "cutoff3"},
        {"x": x, "y": cutoff53, "name": "cutoff5"},
        {"x": x, "y": best, "name": "best"}
]
