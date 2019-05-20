import numpy as np
print(result["chains"].shape)
np.savetxt(output_file, result["chains"])
return
