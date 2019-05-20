import numpy as np
Bprob = np.around(fwd_bwd_result["Bprob"], decimals=8)
a = np.nonzero(Bprob)
b = Bprob[a]
c = np.concatenate((a,b), axis=1)
np.savetxt(output_file+'-Bprob.txt', c,fmt='%.8f')
return
