npz=$1  x-2frag_zA.npz
dat=$2
radii=$3
echo "ok"
npy=$4
list=$5 #UUU-clust1Ar.list
nposes=$6
s=$7        #spacing between non-clashing connected poses
x=${npz%.*}

clust_attract_all(){
  dat=$1
  radii=$2
  list=$3
  ligandr=`head -n 1 $list`
  i=`awk 'NR==1' $radii`
  j=`awk 'NR==2' $radii`

  echo "fastclustering $i A"
  python $ATTRACTDIR/fastcluster.py $dat $ligandr $i --ens 2 $list > $x.clust${i}A

  echo "fast sub-clustering $j A"
  python $ATTRACTDIR/fastsubcluster.py $dat $x.clust${i}A $ligandr $j $x.clust${i}A.subclust${j}A $x.clust${i}A.superclust${j}A --ens 2 $list

  for k in `head -n -2 $radii|tail -n +3`; do
    echo "fast sub-clustering $k A"
    python $ATTRACTDIR/fastsubcluster.py $dat $x.clust${i}A.subclust${j}A $ligandr $k $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
    i=$j; j=$k
  done

  k=`tail -n -1 $radii`
  echo "subclustering $k A"
  python $ATTRACTDIR/subcluster.py $dat $x.clust${i}A.subclust${j}A $ligandr 2 $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
}

clust_attract(){
  dat=$1
  list=$2
  ligandr=`head -n 1 $list`
  N=`tail -n 8 $dat|awk 'NF==1{print substr($1, 2, 10)}'`

  if [ ! $N -gt 10000];then


  echo "fastclustering $i A"
  python $ATTRACTDIR/fastcluster.py $dat $ligandr $i --ens 2 $list > $x.clust${i}A

  echo "fast sub-clustering $j A"
  python $ATTRACTDIR/fastsubcluster.py $dat $x.clust${i}A $ligandr $j $x.clust${i}A.subclust${j}A $x.clust${i}A.superclust${j}A --ens 2 $list

  for k in `head -n -2 $radii|tail -n +3`; do
    echo "fast sub-clustering $k A"
    python $ATTRACTDIR/fastsubcluster.py $dat $x.clust${i}A.subclust${j}A $ligandr $k $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
    i=$j; j=$k
  done

  k=`tail -n -1 $radii`
  echo "subclustering $k A"
  python $ATTRACTDIR/subcluster.py $dat $x.clust${i}A.subclust${j}A $ligandr 2 $x.clust${j}A.subclust${k}A $x.clust${j}A.superclust${k}A --ens 2 $list
}

# creates $x_connected-spacing$s.list  $x_connected-spacing$s.npz
echo "mapnpz-homo"
#$SCRIPTS/mapnpz-homo.py $npz $nposes $s

y=$x\_connected-spacing$s
#select-struct-npy.py $x.npy $y.list  $y.npy
N=`cat $y.list|wc -l`
if [ $N -gt 10000 ];then
  python $ATTRACTTOOLS/select-structures.py  $dat -f $y.list > $y.dat
  echo "clustering"
  #$SCRIPTS/subcluster-npy.sh $y.npy $radii
  clust_attract $y.dat $radii $list

  cat /dev/null > superclust.list
    i=`awk 'NR==1' $radii`
    echo "$x.clust${i}A" > subclust.list
    nradii=`cat $radii|wc -l`
    for n in `seq $nradii`:
      i=`awk -v n=$n 'NR==n' $radii`
      j=`awk -v n=$n 'NR==n+1' $radii`
      echo "$x.clust${i}A.subclust${j}A" >> subclust.list
      echo "$x.clust${i}A.superclust${j}A" >> superclust.list
    done  #print clusters lists

    echo "computing cliques"
    cliques-homo-selection-multiproc.py $npy $y.list 1 $radii `cat subclust.list` `cat superclust.list` $y.npz > $x.cliques
fi
