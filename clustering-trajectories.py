#!/usr/bin/python2.6

'''
old script from LBPA
Convergence assessment by population of clusters
'''
###########################
###  L I B R A R I E S  ###
###########################
import os	# system, popen, path
import string	# split,

RMSD=[]
Ref=[]
with open("RefStructures","r") as RefStructures:
	R=RefStructures.readlines()
	for i in range(len(R)):
		ref = int(R[i].replace("\n",""))
		Ref.append(ref)

for indexStructure in Ref:
	RMSD.append([])
	with open("CA_%i.rms"%(indexStructure),"r") as CA:
		f=CA.readlines()
		for i in range(74000):
			rmsd = float(f[i].split(".00 ")[1].replace(" ","")[:-1])
			RMSD[-1].append(rmsd)

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
	for ref in range(len(Ref)):
		population[traj].append(cluster[bornes[traj]:bornes[traj+1]].count(ref))

with open("cluster","w") as Cluster:
	for i in range(len(cluster)):
		Cluster.write("%i\n"%cluster[i])

with open("populations","w") as populations:
	for ref in Ref:
		populations.write("\t%s"%ref)
	populations.write("\n")
	for traj in range(7):
		for i in population[traj]:
			populations.write("\t%i"%i)
		populations.write("\n")
