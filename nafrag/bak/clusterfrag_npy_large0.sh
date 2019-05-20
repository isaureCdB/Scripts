m=$1

# previously applied deredundant cutoff.
dr=$2

# previously applied tight clustering cutoff
cut1=$3

# newly applied large clustering cutoff
cut2=$4

>&2 echo "cluster at $cut2 A "

# Super-cluster the 1A-cluster centers at 2A
if [ ! -s $name-clust${cut2} ];then
  python3 $d/cluster-npy.py $name-clust${cut1}.npy 2 > /dev/null
  awk '{print $4}' $m-clust${cut1} > $m-clust${cut1}.list
  $d/map_cluster.py $name-clust${cut1}-clust${cut2} $m-clust${cut1}.list > $m-clust${cut2}
fi

rm $name-clust3.0 $name-clust3.0.npy $name-superclust${cut1} $name-clust${cut1}.npy
rm $name-clust${cut1}-clust${cut2}.npy $name-clust${cut1}-clust${cut2} $m-clust${cut1}.list $name-clust${cut1} $m-aa-fit-clust${dr}.npy
