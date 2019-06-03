import numpy as np

boltzmann = float(3.2976230  * 6.022140857 * 10**(-4))
RT = boltzmann * float(310)

print(123)
interactions = map_npz(npz_file)[0]
print("Interactions mapped")
nfrags = len(interactions) + 1

#Storing the energy values
energies = np.array(store_energies(scores_file, RT))
print("Scores stored")
nposes = len(energies)   # total Nb poses

#The forward-backward algorithm
z = fwd(energies, interactions)
y = bwd(energies, interactions)

#print(z)
#print(y)
#The Big "Z"
Z = sum(energies * z[0,:])
print("Big Z2 calculated : %s"%Z)
#Y = sum(y[:,-1])
#print("Big Y2 calculated : %s"%Y)

#Calculating the value of E(p*) per fragment
E = y*energies*z # E[pose, frag]
#print("E %s"%E)

Bprob = np.sum(E, axis = 0)/np.sum(E, axis = (0,1))
print("Bprob %s"%Bprob)

result = {
    "energies": energies,
    "z": z,
    "interactions": interactions,
    "Bprob": Bprob
}
return result
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/cell-fwd-bwd.py
