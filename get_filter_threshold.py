#!/usr/bin/env python3

import numpy as np, sys

scores = np.load(sys.argv[1])
Ntokeep = int(sys.argv[2])

scores.sort(axis=0)
print(scores[Ntokeep][0])
