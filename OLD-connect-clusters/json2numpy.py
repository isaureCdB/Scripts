#!/usr/bin/env python

import sys
import json
import numpy as np

input, output = sys.argv[1:]
data = json.load(open(input))
arrays = {
    "nfrags": np.array(data["nfrags"]),
    "max_rmsd": np.array(data["max_rmsd"])
}
for dnr, d in enumerate(data["clusters"]):
    ar = np.array([dd["ranks"][0] for dd in d])
    arrays["clusters-%i"%dnr] = ar
for dnr, d in enumerate(data["interactions"]):
    ar = np.array(d)
    arrays["interactions-%i"%dnr] = ar
np.savez(output, **arrays)
