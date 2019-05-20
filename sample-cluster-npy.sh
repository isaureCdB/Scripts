echo ""
echo "usage: sample-cluster.sh file.npy template.pdb cutoff"
echo ""
npy=$1
template=$2
cut=$3

name=${npy%%.npy}
npy2pdb.py $npy $template > ${name}_all.pdb
splitmodel ${name}_all.pdb /tmp/$name > ${name}_all.list
a=`cat ${name}_all.list|wc -l`

python $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/..//structure-single.dat \
    $a 2 all > ens.dat

echo '**************************************************************'
echo 'cluster'
echo '**************************************************************'
$ATTRACTDIR/matrix-lrmsd ens.dat /dev/null /tmp/$name-1.pdb --ens 2 ${name}_all.list   > $name.lrmsdlist

# parameters < RMSD cutoff in A> <minimum size of cluster>
$ATTRACTDIR/cluster_struc $name.lrmsdlist $cut 1 > $name.clust${cut}A
awk '{print $4}' $name.clust${cut}A > $name-clust${cut}A.center
select-struct-npy.py $npy --structure `cat $name-clust${cut}A.center` > $name-clust${cut}A.npy
