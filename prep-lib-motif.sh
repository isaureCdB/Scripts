motif=$1
mkdir -p $motif
i=${motif:0:1}
j=${motif:1:1}
k=${motif:2:1}
echo $i $j $k
#
grep ATOM $ATTRACTDIR/../allatom/rnalib/$i-aa.pdb > $motif.pdb
grep ATOM $ATTRACTDIR/../allatom/rnalib/$j-aa.pdb >> $motif.pdb
grep ATOM $ATTRACTDIR/../allatom/rnalib/$k-aa.pdb >> $motif.pdb

python2 $ATTRACTTOOLS/../allatom/aareduce.py $motif.pdb --rna --heavy > /dev/null
npy2pdb.py $motif-aa.npy $motif-aa.pdb > /tmp/$motif-aa-multi.pdb
$ATTRACTTOOLS/splitmodel /tmp/$motif-aa-multi.pdb $motif/conf-aa > $motif-aa.list

python2 $ATTRACTTOOLS/reduce.py $motif-aa.pdb --rna > /dev/null
npy2pdb.py ${motif}r.npy ${motif}r.pdb > /tmp/${motif}r-multi.pdb
$ATTRACTTOOLS/splitmodel /tmp/${motif}r-multi.pdb $motif/confr > ${motif}r.list
