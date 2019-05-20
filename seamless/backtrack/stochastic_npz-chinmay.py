import sys
import numpy as np
import json
import math
import random

def map_npz(jsonfile):
    j = np.load(npz_file)
    nfrags = j['nfrags']
    interactions = [j['interactions-%i'%i] for i in range(1, nfrags-1)]
    clusters = [j['clusters-%i'%i] for i in range(1, nfrags)]
    poses = [ [ int(i)-1 for i in cluster] for cluster in clusters]
    mapped_interactions = [[[poses[i][j[0]], poses[i+1][j[1]]] for j in interactions[i]] for i in range(len(interactions))]
    j = []  # to free memory
    return mapped_interactions, poses


def store_pose_numbers(sel_file):
	f = open(sel_file,"r")
	pose_number = []
	for x in f.readlines():
		pose_number.append(int(x.split(" ")[0]))
	f.close()
	return pose_number

def store_scores(scores_file, n, RT):
	f = open(scores_file,"r")
	scores = [float(l) for l in f.readlines()]
	energies = []
	for i in range(n):
		energies.append(scores[i]/RT)
	f.close
	return energies

def create_graph(interactions, energies, num_inter):
	graph = [[] for i in range(num_inter)]
	for i in range(num_inter):
		for inter in interactions[i]:
			p1 = inter[0]
			p2 = inter[1]
			graph[i].append(math.exp(-energies[p2]))
	return graph

def find_neighbours(interactions, p, internum):
	neighbours = []
	for inter in interactions[internum]:
		if inter[0] == p:
			neighbours.append(inter[1])
	return neighbours


def fwd(graph, interactions, energies):
	zbar = np.zeros((n,nfrags))
	for i in range(n):
		zbar[i][0] = 1.0

	for m in range(1,nfrags):
		for i in range(len(interactions[nfrags-m-1])):
			previouselem = interactions[nfrags-m-1][i][0]
			nextelem = interactions[nfrags-m-1][i][1]
			zbar[previouselem][m] += (graph[nfrags-m-1][i] * zbar[nextelem][m-1])
	return zbar


def stochastic_backtrack_rec(p,m,z,interactions):
	if m==0:
		return []
	number = random.random() * z[p][m]
	neighbours = find_neighbours(interactions, p, nfrags-m-1)
	for q in neighbours:
		number -= (math.exp(-energies[q]) * z[q][m-1])
		if number<0:
			return [q] + stochastic_backtrack_rec(q,m-1,z, interactions)


def stochastic_backtrack(S,z,interactions):
	number = random.random()*S
	for p in poses_list:
		number -= (math.exp(-energies[p]) * z[p][nfrags-1])
		if number<0:
			return [p] + stochastic_backtrack_rec(p,nfrags-1,z, interactions)



if __name__ == "__main__":
	npz_file = sys.argv[1]
	scores_file = sys.argv[2]
	#sel_file = sys.argv[3]
	output_file = sys.argv[3]
	NUM_SAMPLES = int(sys.argv[4])

	boltzmann = float(3.2976230 * (10**(-27)) * (6.022140857 * 10**(23)))
	RT = boltzmann * float(310)

	interactions, poses = map_npz(npz_file)
	print "Interactions mapped"

	poses_list =  [item for sublist in poses for item in sublist]


	#Storing the actual pose numbers
	#pose_number = store_pose_numbers(sel_file)
	#print "Pose numbers stored"

	num_inter = len(interactions)
	nfrags = len(poses)
	n = 500000

	#Storing the energy values
	energies = store_scores(scores_file,n, RT)
	print "Scores stored"

	#Creating the connectivity graph
	graph = create_graph(interactions, energies, num_inter)
	print "Graph created"

	#The forward algorithm
	z = fwd(graph, interactions, energies)

	#The Big "Z"
	Z = 0.0
	for i in range(num_inter):
		for inter in interactions[i]:
			temp_energy = math.exp(-energies[inter[0]])
			Z = Z + (temp_energy * z[inter[0]][nfrags-1])
	print "Big Z calculated"

	#===============================================
	#   Stochastic Backtracking
	#===============================================

	S = sum([math.exp(-energies[p])*z[p][nfrags-1] for p in poses_list])

	for i in range(NUM_SAMPLES):
		print stochastic_backtrack(S, z, interactions)
	print "Backtracking done"
