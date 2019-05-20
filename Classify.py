#!/usr/bin/python2.6
#
# Classification des conformations d'un modèle "struct.pdb"
# issues de plusieurs trajectoires concaténées en une traj "struct.binpos"
#
# Ce code fait appel au module Ptraj de AMBER (dispo via http://ambermd.org/AmberTools-get.html)
#
# La génération des groupe inclu une part de hasare dans le choix des centres de groupe ("refstructures")
# => Reproduire chaque classification plusieurs fois pour une étude statistique des résultats.
#
# Pour ne considérer qu'une partie du modèle (par ex les Calpha),
# il est beaucoup plus rapide d'extraire une nouvelle traj ("struct_Ca.binpos")
# ne contenant que cette partie et faire les calculs dessus
# plutôt que d'utiliser "strip" (cf ci-après) à chaque étape.
#
###########################
###  L I B R A R I E S  ###
###########################
import sys	# argv, exit, stdin
import os	# system, popen, path
import string	# split,
import random

dc = float(sys.argv[1])		# distance seuil (rmsd minimal entre 2 centres de groupes).  
				# A moduler pour obtenir le nb de reférences désiré à chaque classification
Ntraj=int(sys.argv[2])		# Nb de traj (de même taille) concaténées. 
Nconf=int(sys.argv[3])		# Nb de conformations dans chaque traj
Ntot=Ntraj*Nconf
indexStructuresRef=[]		# Liste des refstructures (centres des groupes)
seq=range(1,Ntot+1)
RMSD=[]				# tableau des rmsd de chaque conformation pour chaque refstructure

while (len(seq)>0):
	RMSD.append([])
	indexStructure = random.choice(seq)		# choix aléatoire d'une refstructure dans les Ntot conformations
	indexStructuresRef.append(indexStructure)
	print(indexStructure)
# extraction de la refstructure
	with open("Ptraj_ExtractRef","w") as fileE:
		fileE.write("struct.pdb <<!\n")
		fileE.write("trajin struct.binpos %i %i 1\n"%(indexStructure,indexStructure))
#		fileE.write("strip ~@CA\n")	# ne garder que les C alpha (optionnel, cf ci-dessus)		
		fileE.write("trajout refStruct_%i.pdb pdb\n"%(indexStructure))			
		fileE.write("go")
   	os.system("chmod 777 Ptraj_ExtractRef")
	os.system("./Ptraj_ExtractRef > Ptraj_ExtractRef.log")
	os.system("mv refStruct_%i.pdb.%i refStruct_%i.pdb"%(indexStructure,indexStructure,indexStructure))
# Calcul du RMSD de chaque conformation par rapport a la refstructure, avec Ptraj
	with open ("Ptraj_RMSD","w") as fileR:
		fileR.write("/usr/bin/AmberTOOLS/amber12/bin/ptraj struct.pdb <<!\n")
		fileR.write("trajin struct.binpos\n")
#		fileR.write("strip ~@CA\n")	# ne garder que les C alpha (optionnel, cf ci-dessus)		
		fileR.write("reference refStruct_%i.pdb\n"%(indexStructure))
		fileR.write("rms nofit reference out CA_%i.rms\ngo"%(indexStructure))	
   	os.system("chmod 777 Ptraj_RMSD")
	os.system("./Ptraj_RMSD > Ptraj_RMSD.log")
	
	newSeq=[]
# Tri des conformations situées à plus de dc de RMSD des Refstructures extraites
	with open("CA_%i.rms"%(indexStructure),"r") as CA:
		f=CA.readlines()
		for i in range(Ntot):
			rmsd = float(f[i].split(".00 ")[1].replace(" ","")[:-1])
			RMSD[len(indexStructuresRef)-1].append(rmsd)
			if((rmsd>=dc)&(i in seq)):
				newSeq.append(i)
	seq=newSeq
	print("Conformations encore dans le pool apres %i étapes"%len(indexStructuresRef))
	print(len(seq))

file = open("RefStructures","w")
for i in range(len(indexStructuresRef)):
	file.write("%i\n"%(indexStructuresRef[i]))
file.close()
	
#####################################################################################
#		CLUSTERING
#####################################################################################
cluster=[]
bornes=[]
j=0
for i in range(Ntraj):
	borne.append(j)
	j=j+Nconf

for i in range(Ntot):
	values=[]
	for j in range(len(RMSD)):
		values.append(RMSD[j][i])
	value=max(values)
	index=values.index(value)+1
	cluster.append(index)

population=[]
for traj in range(Ntraj):
	population.append([])
	population[traj]=[]
	for ref in range(len(indexStructuresRef)):
		population[traj].append(cluster[(bornes[traj]):bornes[traj+1]].count(ref))

with open("populations","w") as populations:
        for ref in indexStructuresRef:
                populations.write("\t%s"%ref)
        populations.write("\n")
        for pop in population:
                for p in pop:
                        populations.write("\t%i"%p)
                populations.write("\n")
