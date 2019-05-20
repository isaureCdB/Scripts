import pandas as pd
from io import StringIO
import copy

df = pd.read_csv(StringIO(csv))
complexes = df.complex.unique()
attrib = [
  {
    "type": 'scatter',
    "showlegend": False,
  },
]
series = {
    "type": 'scatter',
    "mode": 'markers',
    "marker": {
        "size": 10
    }
}
symbol_extremity = "triangle-up"
symbol_center = "square"
colstep = 360.0/len(complexes)
hsv_l = [40, 70]
hsv_s = [80,100]
for cindex, complex in enumerate(complexes):
    myseries = copy.deepcopy(series)
    cdf = df[df.complex==complex]
    markers = []
    texts = []
    for n in cdf.index:
        frag = cdf.fragment[n]
        texts.append("frag" + str(frag))
        if frag == 1 or n == cdf.index[-1]:
            markers.append(symbol_extremity)
        else:
            markers.append(symbol_center)
    myseries["marker"].update({"symbol": markers})
    myseries["name"] = complex
    myseries["text"] = texts
    saturation = hsv_s[cindex%2]
    lightness = hsv_l[cindex%2]
    col = "hsl(%.3f,%s,%s)"%(colstep*(2*int(cindex/2)), saturation, lightness)
    myseries["marker"]["color"] = col
    attrib.append(myseries)

return attrib
