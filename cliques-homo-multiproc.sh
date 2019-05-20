npz=$1 #UUU-e6-8frag-1.3.npz
npy=$2 #UUU-e6.npy
radii=$3

x=${npz%.*}
list=$motif\r.list
ligandr=`head -n 1 $list`

$SCRIPTS/select_connected.py $npz > $x.connected
echo "selection structures"
python $ATTRACTTOOLS/select-structures-npy.py $npy `cat $x.connected` > $x-connected.npy
i=`awk 'NR==1' $radii`
j=`awk 'NR==2' $radii`

$SCRIPTS/subcluster-npy.sh $x-connected.npy $radii

echo "$x.clust${j}A.superclust${k}A" >> superclust.list
echo "$x.clust${j}A.subclust${k}A" >> subclust.list

echo "computing cliques"
cliques-homo-selection-multiproc.py $npy $x.connected 1 $radii `cat subclust.list` `cat superclust.list` $npz > $x.cliques
