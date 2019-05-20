# assemble homo-polymer

# the higher the number of poses, the lower the overlap cutoff, for memory issues (see below)
# ex: 25,000 poses with 3A cutoff needs ~40G memory

name=$1
nfrag=$2
cutoff=$3
maxposes=$4

#############################################################
# compute all frag1-frag2 connections
#############################################################
python connect.py 2 $cutoff $maxposes 100 $name-preatoms.npy $name-preatoms.npy $name-postatoms.npy $name-postatoms.npy  > $name-2frag-${cutoff}A.json

#############################################################
# propagate the possible connections through the homogenous sequence
# !!! needs python3 and python3-numpy !!!
#############################################################
python3 connect-homo.py $name-2frag-${cutoff}A.json $nfrag > $name-${nfrag}-${cutoff}A.json

exit

#############################################################
# for memory issues
#############################################################
# you might need to split the npy array of one fragment, to compute separate connections files
# for (chunks of poses) vs (all poses), then merge them. There are the commands:

#############################################################
#prepare selection files
#############################################################
nlines=$5 # size of you selections
nposes=`python -c 'import numpy as np; a=np.load("'$name'-postatoms.npy");print a.shape[0]'`

j=0
for i in `seq 1 $nlines $nposes`;do
    j=$(($j+1))    
    seq $i $(($i+$nlines-1)) > sel-$j
done
seq $nposes > sel-$nposes

#############################################################
# compute each set of connections
#############################################################
cat dev/null > json.list
for s in `seq $j`; do
    python3 connect.py $nfrag $cutoff $maxposes 100 $name-preatoms.npy $name-preatoms.npy $name-postatoms.npy $name-postatoms.npy sel-$nposes sel-$s > sel-$s.json
    echo "sel-$s.json" >> json.list
done

#############################################################
# merge
#############################################################
# The merging is not trivial, as the connection.json files use their own indexing of poses,
# that is mapped to ATTRACT ranking by the "clusters" list of list of dictionaries:
# clusters[frag_index] = [ {rank: [xxx], radius: 0}, {rank: [yyy], radius: 0} ... ]
python3 concatenate_jsonlist.py `cat json.list` > $name-${nfrag}-${cutoff}A.json

