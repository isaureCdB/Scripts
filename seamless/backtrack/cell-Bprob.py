import numpy as np

E = fwd_bwd_result["E"]

Bprob = E/np.sum(E, axis = 1)[:,None]
print("Bprob computed, saved in %s"%output_file)

#np.savetxt(output_file, fwd_bwd_result["Bprob"],fmt='%.8f')
np.save(output_file, Bprob) #npz_file+".Bprob"

return Bprob
