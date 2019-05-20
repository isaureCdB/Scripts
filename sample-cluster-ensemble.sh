echo ""
echo "usage: sample-cluster.sh structure-file(without ".dat" ) receptor.pdb ligand.pdb cutoff option(best/center) "
echo ""

name=$1
cut=$2
ens=$3

ligand=`head -n 1 $ens`
receptor=/dev/null

echo '**************************************************************'
echo 'cluster'
echo '**************************************************************'
if [ ! -f $name.lrmsdlist ]; then
	$ATTRACTDIR/matrix-lrmsd ens.dat /dev/null $ligand --ens 2 $ens > lrmsdlist
fi

# parameters < RMSD cutoff in A> <minimum size of cluster>
$ATTRACTDIR/cluster_struc lrmsdlist $cut 1 > clust${cut}A
python $ATTRACTTOOLS/cluster2dat.py $name-clust${cut}A $name.dat > $name-clust${cut}A.dat
#$ATTRACTDIR/collect $name-clust${cut}A.dat $receptor $ligand  --ens 2 $ens > $name-clust${cut}A.pdb

#cat $name-cluster.dat |awk '{print $4}' |sort > $name-cluster-centers


