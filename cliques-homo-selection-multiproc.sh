motif=$1
npz=$2
dat=$3
radii=$4
echo "ok"
npy=$5

x=${npz%.*}
list=$motif\r.list
ligandr=`head -n 1 $list`

$SCRIPTS/select_connected.py $npz > $x.connected
echo "selection structures"
python $ATTRACTTOOLS/select-structures.py $dat `cat $x.connected` > $x.dat
i=`awk 'NR==1' $radii`
j=`awk 'NR==2' $radii`

echo "fastclustering $i A"
python $ATTRACTDIR/fastcluster.py $x.dat $ligandr $i --ens 2 $list > $x.clust${i}A

echo "fast sub-clustering $j A"
python $ATTRACTDIR/fastsubcluster.py $x.dat $x.clust${i}A $ligandr $j $x.clust${i}A.subclust${j}A $x.clust${i}A.superclust${j}A --ens 2 $list
echo "$x.clust${i}A" > subclust.list
echo "$x.clust${i}A.subclust${j}A" >> subclust.list
echo "$x.clust${i}A.superclust${j}A" > superclust.list

#for k in `awk '{for (i=3;i<NF;i++){print $i}}' $radii`; do
for k in `head -n -2 $radii|tail -n +3`; do
  echo "fast sub-clustering $k A"
  python $ATTRACTDIR/fastsubcluster.py $x.dat $x.clust${i}A.subclust${j}A $ligandr $k $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
  echo "$x.clust${j}A.subclust${k}A" >> subclust.list
  echo "$x.clust${j}A.superclust${k}A" >> superclust.list
  i=$j
  j=$k
done
k=`tail -n -1 $radii`
echo "subclustering $k A"
python $ATTRACTDIR/subcluster.py $x.dat $x.clust${i}A.subclust${j}A $ligandr 2 $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
echo "$x.clust${j}A.superclust${k}A" >> superclust.list
echo "$x.clust${j}A.subclust${k}A" >> subclust.list

echo "computing cliques"
cliques-greedy-homo.py $npy $x.connected 1 $radii `cat subclust.list` `cat superclust.list` $npz > $x.cliques
