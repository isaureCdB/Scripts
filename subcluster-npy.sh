npy=$1
rmsdlist=$2 # list of RMSD thresholds for hierarchical clustering,orderer from larger to tighter
n=`cat $rmsdlist|wc -l`

n=${npy%.npy}
a=`awk 'NR==1{print $1}' $rmsdlist`

echo "$SCRIPTS/fastcluster_npy.py $n.npy $a --no-assign-structures"
$SCRIPTS/fastcluster_npy.py $n.npy $a --no-assign-structures

for b in `awk -v n=$n 'NR>1&&NR<n{print $1}' $rmsdlist`;do
	echo "$SCRIPTS/fastsubcluster-npy.py $n.npy $n-clust$a $b $n-clust$b $n-superclust$b"
    $SCRIPTS/fastsubcluster_npy.py $n.npy $n-clust$a $b $n-clust$b $n-superclust$b
    a=$b
done

b=`awk -v n=$n 'NR==n{print $1}' $rmsdlist`
$SCRIPTS/subcluster-npy.py $n.npy $n-clust$a $b $n-clust$b $n-superclust$b

