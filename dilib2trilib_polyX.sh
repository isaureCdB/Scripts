SCRIPTS="$PROTNAFF/create_frag_library/"


#select-npy.py ../CCA-all-aa.npy CCA-all-aa-n12.npy  --atoms `seq 38`
#select-npy.py ../ACC-all-aa.npy ACC-all-aa-n23.npy  --atoms `seq 22 59`
#select-npy.py ../CCC-all-aa.npy CCC-all-aa-n12.npy  --atoms `seq 38`
#select-npy.py ../CCC-all-aa.npy CCC-all-aa-n23.npy  --atoms `seq 20 57`

#join-npy.py CC-all-aa.npy CCA-all-aa-n12.npy ACC-all-aa-n23.npy CCC-all-aa-n12.npy CCC-all-aa-n23.npy

./discard_clashing_fragments.py CC-all-aa.npy 19 2 CC-aa-noclash.npy CC-aa-noclash

fit_multi_npy.py CC-aa-noclash.npy CC-aa-fit.npy --first

f=CC-aa-fit
c2=2.0
dr=0.1

python3 $SCRIPTS/fastcluster_npy.py $f.npy $c2 2> fastcluster-$c2.log
python3 $SCRIPTS/concatenate_clusters.py $f-clust$c2 > $f-clust$c2-concat
python3 $SCRIPTS/fastsubcluster_npy.py $f.npy $f-clust$c2-concat $dr $f-noclash-clust$dr /dev/null 2> fastsubcluster-CC-$dr.log
python3 $SCRIPTS/select-struct-npy.py $f.npy $f-clust${dr}.npy --structures `awk '{print $4}' $f-noclash-clust${dr}`

#python3 $SCRIPTS/clustering_hierarchical.py $f-clust${dr}.npy 1.0 1.3 -c 6 -o CC


f=CC-aa-fit-clust${dr}

cat $ATTRACTDIR/../allatom/dnalib/C.pdb > CC.pdb
cat $ATTRACTDIR/../allatom/dnalib/C.pdb >> CC.pdb

fit_multi_npy.py $f.npy $f-fitted-nucl1.npy --pdb CC.pdb --atoms 1 4 5 6 8 10 11 18

fit_multi_npy.py $f.npy $f-fitted-nucl2.npy --pdb CC.pdb --atoms 20 23 24 25 27 29 30 37

select-struct-npy.py $f-fitted-nucl2.npy $f-fitted-nucl2-select-n1.npy --atom 1 4 5 6 8 10 11 18
select-struct-npy.py $f-fitted-nucl1.npy $f-fitted-nucl1-select-n2.npy --atom 20 23 24 25 27 29 30 37

c=0.3
fastcluster_npy.py $f-fitted-nucl2-select-n1.npy $c 
fastcluster_npy.py $f-fitted-nucl1-select-n2.npy $c

o=0.2
./dilib-to-trilib-fitted-dr.py $f-fitted-nucl2.npy $f-fitted-nucl1.npy \
														 $f-fitted-nucl2-select-n1-clust$c $f-fitted-nucl1-select-n2-clust$c \
														 $o 0.2 1 ../CCC-dr0.2r-clust1.0-aa.npy CCC $ATTRACTTOOLS/../allatom/dnalib  \
														 > di2tri-CCC.log 2> di2tri-CCC.err


