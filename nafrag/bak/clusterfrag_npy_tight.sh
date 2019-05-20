name=$1 # $m-dr${dr}r
m=$2  # sequence motif
cut=$3 # Clustering cutoff

d=`dirname "$0"`

set -u -e

# Cluster fragments by RMSD.
# Hierarchical clustering (for speed & memory): first cluster at a = (cut + 2) A,
# then sub-cluster each ${a}A-cluster members at $cut A
a=`echo $cut + 2|bc`
>&2 echo "-------------------------------------------------"
>&2 echo "Cluster $m large ($a A); then tight ($cut A)"
>&2 echo "-------------------------------------------------"

>&2 echo "cluster $m large $m ($a A)"
python3 $d/fastcluster_npy.py $name.npy $a --chunk 200

>&2 echo "cluster $m tight $m ($cut A)"
python3 $d/subcluster-npy.py $name.npy $name-clust${a} $cut > /dev/null

sel=`awk '{print $4}' $name-clust$cut`
$d/select-struct-npy.py $name.npy $m-clust$cut.npy --structure $sel

# Map indices from non-redundant fragments indices to global fragment indices
$d/map_cluster.py $name-clust$cut $name.list > $m-clust${cut}
awk '{print $4}' $m-clust$cut > $m-clust${cut}.list

rm $name-clust3.0 $name-clust3.0.npy $name-superclust${cut}
rm $m-clust${cut}.list $name-clust${cut}
