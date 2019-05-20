import numpy as np
result = {
    "energies": input["energies"],
    "z": input["z"],
    "interactions": input["interactions"],
}
np.save(output_file, result)
return
