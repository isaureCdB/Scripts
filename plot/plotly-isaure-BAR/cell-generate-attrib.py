import pandas as pd
from io import StringIO
df = pd.read_csv(StringIO(csv))


result = [
    {"type": "bar", "marker": {"color":[]}}, #cutoff3
    {"type": "bar", "marker": {"color":[]}}, #cutoff5
    {"type": "scatter",
    "mode": "markers",
    "marker": {"color": "black"},
    }, #best
]
c3 = result[0]["marker"]["color"]
c5 = result[1]["marker"]["color"]
for row in df.index:
    r = df.ix[row].tolist()
    length0 = r[1].strip()[1:].split("-")
    length = int(length0[1]) - int(length0[0]) + 1
    if length == 7:
        col3 = "hsl(0,100,50)"
        col5 = "hsl(0,70,70)"
    elif length == 6:
        col3 = "hsl(30,100,50)"
        col5 = "hsl(30,90,70)"
    elif length == 5:
        col3 = "hsl(50,90,50)"
        col5 = "hsl(50,90,70)"
    else:
        col3 = "hsl(100,100,50)"
        col5 = "hsl(100,70,70)"
    c3.append(col3)
    c5.append(col5)
return result
