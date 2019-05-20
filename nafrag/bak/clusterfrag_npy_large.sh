name=$1
m=$2
cut=$3
d=`dirname "$0"`

>&2 echo "cluster $name at $cut A "

# Super-cluster the 1A-cluster centers at 2A
python3 $d/cluster-npy.py $name.npy 2 > /dev/null
awk '{print $4}' $name > $name.list
$d/map_cluster.py $name-clust${cut} $name.list > $m-clust${cut}

rm $name-clust${cut} $name.list
