import random
import time
import numpy as np

start = time.time()
energies, z, interactions = \
  fwd_bwd_result["energies"], \
  fwd_bwd_result["z"], fwd_bwd_result["interactions"]

Z = sum(energies * z[0,:])

print("will sample %s chains"%num_samples)
np.random.seed(0)
chains, occurencies = stochastic_backtrack(energies, Z, z, interactions, num_samples)
stop = time.time()

counted = sorted(list(zip(occurencies, chains)), key=lambda k: -k[0])
#for count, chain in counted:
#    print(count, "   ", *chain, file=result)

print("time : %s"%(stop - start))
print("DONE")
result = {
    "chains": counted,
}
return result
