echo ""
echo "usage: sample-cluster.sh structure.dat receptor.pdb ligand.pdb cutoff option(best/center) "
echo ""
name=${1%%.dat}
receptor=$2
ligand=$3
cut=$4
#option=$5	 # Select "best" or "center" in each cluster

echo '**************************************************************'
echo 'cluster'
echo '**************************************************************'
if [ ! -f $name.lrmsdlist ]; then
	$ATTRACTDIR/matrix-lrmsd $name.dat $receptor $ligand  > $name.lrmsdlist
fi

# parameters < RMSD cutoff in A> <minimum size of cluster>
$ATTRACTDIR/cluster_struc $name.lrmsdlist $cut 1 > $name-clust${cut}A
python $ATTRACTTOOLS/cluster2dat.py $name-clust${cut}A $name.dat --best > $name-clust${cut}A.dat
$ATTRACTTOOLS/top $name-clust${cut}A.dat 100 > $name-clust${cut}A-top100.dat
$ATTRACTDIR/collect $name-clust${cut}A-top100.dat /dev/null $ligand  > $name-clust${cut}A-top100.pdb

#cat $name-cluster.dat |awk '{print $4}' |sort > $name-cluster-centers
