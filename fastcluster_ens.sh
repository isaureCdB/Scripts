dat=$1
list=$2
r=$3 #clustering radius

lim1=10000
lim2=100000

ligandr=`head -n 1 $list`
N=`tail -n 8 $dat|awk 'NF==1{print substr($1, 2, 10)}'`
x=${dat%*.dat}

if [ "$N" -gt "$lim1" ];then
  echo "fastclustering 10 A"
  if [ ! -s $x.clust10A ];then
    python $ATTRACTDIR/fastcluster.py $dat $ligandr 10 --ens 2 $list > $x.clust10A
  fi
  i=10
  while [ "$i" -gt "$r" ] ; do
    j=$(($i-1))
    if [ ! $N -gt $lim2 ]; then
      j=$(($i-4))
    fi
    if [ ! $j -gt $r ]; then
      break
    fi
    echo "fast sub-clustering ${j} A"
    if [ ! -s $x.clust${j}A ];then
      python $ATTRACTDIR/fastsubcluster.py $dat $x.clust${i}A $ligandr 8 $x.clust${j}A $x.superclust${j}A --ens 2 $list
    fi
    i=$j
    N=`awk 'BEGIN{m=0}(NF-3)>m{m=NF-3}END{print m}' $x.clust${i}A`
  done
  python $ATTRACTDIR/subcluster.py $dat $x.clust${i}A $ligandr $r $x.clust${r}A $x.superclust${r}A --ens 2 $list
else
  if [ ! -f $x.lrmsdlist ]; then
	   $ATTRACTDIR/matrix-lrmsd $dat /dev/null $ligandr --ens 2 $list > $x.lrmsdlist
  fi
  $ATTRACTDIR/cluster_struc $x.lrmsdlist $r 1 > $x.clust${r}A
fi
