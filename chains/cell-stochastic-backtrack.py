import random
import time
import numpy as np

start = time.time()
energies, z, interactions = \
  fwd_bwd_result["energies"], \
  fwd_bwd_result["z"], fwd_bwd_result["interactions"]

Z = sum(energies * z[0,:])

np.random.seed(0)
chains, occurencies = stochastic_backtrack(energies, Z, z, interactions, num_samples)
stop = time.time()

counted = sorted(list(zip(occurencies, chains)), key=lambda k: -k[0])
chains_sorted = np.array([c[1] for c in counted])
occurencies_sorted =  np.array([c[0] for c in counted])
#for count, chain in counted:
#    print(count, "   ", *chain, file=result)

print("time : %s"%(stop - start))
print("DONE")
result = {
    "chains": chains_sorted,
    "occurencies": occurencies_sorted
}
return result
