#!/usr/bin/python2.6

###########################
###  L I B R A R I E S  ###
###########################
import sys	# argv, exit, stdin
import os	# system, popen, path
import string	# split,
import random

dc = float(sys.argv[1])		# distance cutoff (rmsd minimial)
indexStructuresRef=[]		# Liste des refstructures (qui seront les centres de clusters)
seq=range(1,74001)
indexStructuresRef=[]		# Liste des refstructures (qui seront les centres de clusters)
RMSD=[]		# tableau des rmsd(snapshot)/reference pour chaque traj et chaque reference

while (len(seq)>0):
	RMSD.append([])
	indexStructure = random.choice(seq)	# choix d'une refstructure dans les 74000 conformations
	indexStructuresRef.append(indexStructure)
	print(indexStructure)
# extraction de la refstructure: on va rechercher dans quelle trajectoire se trouve la refstructure piochee.
	with open("Ptraj_ExtractRef","w") as fileE:
		fileE.write("/home/isaure/bin/AmberTOOLS/amber12/bin/ptraj /home/isaure/MD/bb.pdb <<!\n")
		fileE.write("trajin /home/isaure/MD/binpos/bb/wvhyngd_centerdt10_CACNO.binpos %i %i 1\n"%(indexStructure,indexStructure))
		fileE.write("strip :1-2,327-331\n")	#On retire les extremitees les plus fluctuantes (cf "wvhyngd_centerdt10_CACNO")
		fileE.write("trajout refStruct_%i.pdb pdb\n"%(indexStructure))			
		fileE.write("go")
   	os.system("chmod 777 Ptraj_ExtractRef")
	os.system("./Ptraj_ExtractRef > Ptraj_ExtractRef.log")
	os.system("mv refStruct_%i.pdb.%i refStruct_%i.pdb"%(indexStructure,indexStructure,indexStructure))
# On va calculer le RMSD de chaque conformation par rapport a la refstructure, avec Ptraj
	with open ("Ptraj_RMSD","w") as fileR:
		fileR.write("/home/isaure/bin/AmberTOOLS/amber12/bin/ptraj /home/isaure/MD/bb.pdb <<!\n")
		fileR.write("trajin /home/isaure/MD/binpos/bb/wvhyngd_centerdt10_CACNO.binpos\n")
		fileR.write("strip :1-2,327-331\n")	#On retire les extremitees
		fileR.write("reference refStruct_%i.pdb\n"%(indexStructure))
		fileR.write("rms reference out CA_%i.rms\ngo"%(indexStructure))	
   	os.system("chmod 777 Ptraj_RMSD")
	os.system("./Ptraj_RMSD > Ptraj_RMSD.log")
	
	newSeq=[]
	with open("CA_%i.rms"%(indexStructure),"r") as CA:
		f=CA.readlines()
		for i in range(74000):
			rmsd = float(f[i].split(".00 ")[1].replace(" ","")[:-1])
			RMSD[len(indexStructuresRef)-1].append(rmsd)
			if((rmsd>=dc)&(i in seq)):
				newSeq.append(i)
	seq=newSeq
	print("Conformations encore dans le pool apres %i etapes"%len(indexStructuresRef))
	print(len(seq))

file = open("RefStructures","w")
for i in range(len(indexStructuresRef)):
	file.write("%i\n"%(indexStructuresRef[i]))
file.close()
	
#####################################################################################
#		CLUSTERING
#####################################################################################
cluster=[]
bornes=[0,9600,19200,28800,38400,48000,61000,74000]
for i in range(74000):
	values=[]
	for j in range(len(RMSD)):
		values.append(RMSD[j][i])
	value=min(values)
	index=values.index(value)
	cluster.append(index)

population=[]
for traj in range(7):
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


