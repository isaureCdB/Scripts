#/bin/bash
set -u

# adapted from connect-homopolymer.sh

preatoms=$1 #in .npy format
postatoms=$2
cutoff=$3 #overlap RMSD cutoff
chunksize=$4 #number of structures to connect against the full npy
simultaneous=$5 #number of connect jobs to run in parallel
outputfile=$6  #outputfile in JSON format

#############################################################
# for memory issues
#############################################################
# you might need to split the npy array of one fragment, to compute separate connections files
# for (chunks of poses) vs (all poses), then merge them. There are the commands:

#############################################################
#prepare selection files
#############################################################
nposes=`python -c 'import numpy as np; a=np.load("'$preatoms'");print a.shape[0]'`

j=0
cat /dev/null > sel-chunk-json.list
for i in `seq 1 $chunksize $nposes`;do
    j=$(($j+1))
    seq $i $(($i+$chunksize-1)) > sel-chunk-$j
    echo "sel-chunk-$j.json" >> sel-chunk-json.list
done
seq $nposes > sel-$nposes

#############################################################
# compute each set of connections
#############################################################
echo $j $simultaneous
for s in `seq $j`; do
    echo connect.py chunk $s >> /dev/stderr
    python $SCRIPTS/connect.py 2 $cutoff 999999999 100 $preatoms $preatoms $postatoms $postatoms sel-$nposes sel-chunk-$s > sel-chunk-$s.json 2> sel-chunk-$s.log &
    ((i=i%simultaneous)); ((i++==0)) && wait && echo WAIT
done
wait

#############################################################
# merge
#############################################################
# The merging is not trivial, as the connection.json files use their own indexing of poses,
# that is mapped to ATTRACT ranking by the "clusters" list of list of dictionaries:
# clusters[frag_index] = [ {rank: [xxx], radius: 0}, {rank: [yyy], radius: 0} ... ]
python3 $SCRIPTS/concatenate_jsonlist.py `cat sel-chunk-json.list` > $outputfile
#rm -f sel-chunk-*
