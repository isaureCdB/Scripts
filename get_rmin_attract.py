#!/usr/env python

# Search the minimum of the difference (optimal_distance - real_distance)
# by iterating over all Rbead-Lbead pairs (R for Receptor, L for Ligand)
# Usage: python get_best_airing_annotated-1.py pdbfile1 pdbfile2 >  output

# numpy (for "numerical python") is an extension to the Python programming language,
# adding support for large, multi-dimensional arrays and matrices,
# and a large library of high-level mathematical functions to operate on these arrays.
# Function from numpy will be called by : np.function(input)
# or for some of them by a shortcut: input.function
import numpy as np

# scipy (for "scientific python") another python library that adds more MATLAB-like functionality
from scipy.spatial.distance import cdist

import sys
###########################################################################
# compute the optimal Rbead - Lbead distances in ATTRACT parameters
###########################################################################

# to give python direct access to attract scripts and data
import os
attract = os.environ["ATTRACTDIR"]

parfile = attract+"/../attract.par"
lines = open(parfile).readlines()  # gives the list of lines in a text file.
firstline = lines[0] 
firstline_data = firstline.split() # list of strings in the line (separated by space)
potshape = int(firstline_data[0])  # transform string into integer
N = int(firstline_data[1])  # Number of parameters per line

# for your information ("FYI"), you can also combine all those commands:
potshape = int( open(parfile).readlines()[0].split()[0] )

# the function np.loadtxt loads a text array and transforms it into a binary array
parmlines = open(parfile).readlines()
Nb_lines = len(parmlines)
parameters = []
i = 0
for line in parmlines[1:]:  # we skip the 1st line
    items = line.split()
    j = 0
    p = []
    for item in items:
        p.append(float(item)) # add item to a list
        j += 1
    parameters.append(p) # add list to a list of lists
    i +=1

# convert the txt array into a binary array, for fast computations.
parm = np.array(parameters)

# shape is a numpy function
# np.shape(matrix) = (Nb_rows in matrix, Nb_columns in matrix) 
parm_Nrow, parm_Ncol = np.shape(parm)[0], np.shape(parm)[1]

#####################
# This command is to print in your terminal, instead of in your ouput files.
# VERY VERY usefull for debuging: to check lengths of lists, dimensions of matrices...

# %i for integer, %f for float, %s for string...
print >> sys.stderr, "parameters : %i lines, %i columns" %(parm_Nrow, parm_Ncol)
# you should have 3*N rows and N columns
#####################

# initialize a matrix of zeros, in which we'll store the optimal distances
rmin = np.zeros((N,N))
   
rbc = parm[:N]
abc = parm[N:2*N]
ipon = parm[2*N:3*N]

rc = abc*rbc**potshape
ac = abc*rbc**6  # ac <= 0 for non-compatible beads

# creates a boolean matrix with same dimension (or shape) as ac:
# if ac[i,j] > 0:
#     mask[i, j] = True 
# else:
#     mask[i, j] = False   
mask_compatible = ac > 0

# matrix[mask] extracts from matrix only the part corresponding to True areas of mask.
rmin[mask_compatible] = (4*rc[mask_compatible]/(3*ac[mask_compatible]))**0.5

# if the beads are repulsive, we set the optimal distance to 0
mask_repulsive = ipon == -1
rmin[mask_repulsive] = 0

###########################################################################
# Parse the command-line arguments
###########################################################################
def pdbparse(pdbfile):
    pdb = [ l for l in open(pdbfile).readlines() if l.startswith("ATOM") ]
    coord_array = []
    for l in pdb:
        x, y, z = float(l[30:38]),float(l[38:46]),float(l[46:54])
        coordinates = [x, y, z]
        coord_array.append(coordinates)
    # you can also create arrays by python's "list comprehension":
    # coord_array = [ [float(l[30:38]),float(l[38:46]),float(l[46:54])] for l in pdb]
    # That is what is used below:
    beadtype =  [ int(l[57:59]) for l in pdb ]
    Nat = len(pdb) # number of atoms
    return coord_array, beadtype, Nat
    
import sys
pdbfile1 = sys.argv[1]
pdbfile2 = sys.argv[2]

coord1, type1, Nat1 =  pdbparse(pdbfile1)
coord2, type2, Nat2 =  pdbparse(pdbfile2)

###########################################################################
# This part is to find in a protein-protein complex the pair of beads
# the closest to their optimal distance
###########################################################################

# Map each bead-bead pair to the corresponding type-type pair.
def mapp(bead_index1, bead_index2):
    t1, t2 = type1[bead_index1], type2[bead_index2]
    if t1 == 99 or t2 == 99:  # Those 99 beads are not interacting with anything (= "ghost beads")
        return 0
    else:
        return rmin[ t1-1, t2-1 ]  # Optimal distance for this pair

# cdist is a function from SciPy that gives you the distance between two (lists of) points.
# If you give lists of points, it gives you a matrix of distances.
real_distance = cdist(coord1, coord2)

# range(x, y) = [x, x+1, x+2, ..., y-1]
# mind the y-1, not y!
indexes1 = range(Nat1)
indexes2 = range(Nat2)

# This is a list comprehension inside a list comprehension!
# (did you see the "inception" movie?)
optimal_distance = [ [mapp(i,j) for j in indexes2] for i in indexes1 ]

# Returns absolute values. We don't want negative distances!
# ** = to the power of
delta = []
for i in indexes1:
    d = []
    for j in indexes2:
        if optimal_distance[i][j] == 0:  # the bead does not interact
            diff = 1000
        else:
            diff = ((real_distance[i][j] - optimal_distance[i][j])**2)**0.5
        d.append( diff )
    delta.append(d) 

min_value = 10
for i in range(Nat1):
    for j in range(Nat2):
        if delta[i][j] < min_value:
            min_value = delta[i][j]
            bead_pdb1, bead_pdb2  = i+1, j+1 # convert indexes from 0 to index from 1

print "minimal difference of distance : %f"%min_value
print "optimal beads : %i %i"%(bead_pdb1, bead_pdb2) 
print "optimal distance : %f"%real_distance[bead_pdb1-1, bead_pdb2-1 ]



