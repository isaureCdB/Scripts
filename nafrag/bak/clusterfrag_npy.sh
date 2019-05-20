m=$1

# previously applied deredundant cutoff.
dr=$2

# previously applied tight clustering cutoff
cut1=$3

# newly applied large clustering cutoff
cut2=$4

# Super-cluster the 1A-cluster centers at 2A
if [ ! -s $m-dr0.2r-clust2.0 ];then

  python3 $d/cluster-npy.py $m-dr0.2r-clust1.0.npy 2 > /dev/null
  awk '{print $4}' $m-clust1.0 > $m-clust1.0.list
  $d/map_cluster.py $m-dr0.2r-clust1.0-clust2.0 $m-clust1.0.list > $m-clust2.0
fi

rm $m-dr0.2r-clust3.0 $m-dr0.2r-clust3.0.npy $m-dr0.2r-superclust1.0 $m-dr0.2r-clust1.0.npy
rm $m-dr0.2r-clust1.0-clust2.0.npy $m-dr0.2r-clust1.0-clust2.0 $m-clust1.0.list $m-dr0.2r-clust1.0 $m-aa-fit-clust0.2.npy
