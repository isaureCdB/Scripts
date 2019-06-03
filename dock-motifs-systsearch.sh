#!/bin/bash -i

np=$1
parals="--np $np --chunks $np"

name=`pwd|awk -F "/" '{print $NF}'`
echo $name

nalib=/data1/isaure/nalib_05_2018/
export ATTRACTTOOLS=/data1/isaure/attract/tools/
export ATTRACTDIR=/data1/isaure/attract/bin/
receptorr=proteinr.pdb

set -u -e

#################################################################################
dock(){
#################################################################################
list=$motif-clust1Ar.list
ligandr=`head -n 1 $list`
Nconf=`cat $list|wc -l`
tmpname=/tmp/$name-$motif
devname=/dev/shm/$name-$motif

echo "dock1 $motif $list"

set -u +e
ln -s $nalib/$list
ln -s $nalib/$motif
set -u -e

gridparams=" --grid 1 receptorgrid.gridheader"
params="$ATTRACTDIR/../attract.par $receptorr $ligandr --fix-receptor --ens 2 $list $gridparams $parals"
scoreparams="$ATTRACTDIR/../attract.par $receptorr $ligandr --score --fix-receptor --ens 2 $list --rcut 50 $parals"

if [ ! -s $motif.dat ];then #####################################################
  echo '**************************************************************'
  echo 'calculate receptorgrid grid'
  echo '**************************************************************'
  awk '{print substr($0,58,2)}' $ligandr | sort -nu > receptorgrid.alphabet
  $ATTRACTDIR/make-grid-omp $receptorr $ATTRACTDIR/../attract.par 5.0 7.0 receptorgrid.gridheader  --shm --alphabet receptorgrid.alphabet
  echo '**************************************************************'
  echo 'Generate starting structures...'
  echo '**************************************************************'
  if [ ! -s systsearch.dat ];then
          cat $ATTRACTDIR/../rotation.dat > rotation.dat
          $ATTRACTDIR/translate $receptorr $ligandr > translate.dat
          $ATTRACTDIR/systsearch > systsearch.dat
  fi
  if [ ! -s systsearch-ens-$Nconf.dat ];then
      python2 $ATTRACTTOOLS/ensemblize.py systsearch.dat $Nconf 2 all > systsearch-ens-$Nconf.dat
  fi
  #$ATTRACTTOOLS/top systsearch-ens-$Nconf.dat 10 > top.dat
  #start=top.dat
  start=systsearch-ens-$Nconf.dat
  echo '**************************************************************'
  echo 'docking $motif'
  echo '**************************************************************'
  python2 $ATTRACTDIR/../protocols/attract.py $start $params --vmax 100 --output $motif.dat --pattern $devname
  rm $devname*
fi

echo '**************************************************************'
echo 'scoring $motif'
echo '**************************************************************'
if [ ! -s $motif.score ];then
  python2 $ATTRACTDIR/../protocols/attract.py $motif.dat $scoreparams --output $motif.score --pattern $devname-score
  rm -rf $devname-score*
fi
python2 $ATTRACTTOOLS/fill-energies.py $motif.dat $motif.score > $tmpname-scored.dat

echo '**************************************************************'
echo 'sort & deredundant $motif'
echo '**************************************************************'
### sort structures by score. Also quite time-consuming !
python2 $ATTRACTTOOLS/sort.py $tmpname-scored.dat > $tmpname-sorted.dat
$ATTRACTDIR/fix_receptor $tmpname-sorted.dat 2 --ens 0 $Nconf | python2 $ATTRACTTOOLS/fill.py /dev/stdin $tmpname-sorted.dat > $tmpname-sorted.dat-fixre
### remove redundant structures with worse rank
$ATTRACTDIR/deredundant $tmpname-sorted.dat-fixre 2 --lim 0.1 --radgyr 6 --ens 0 $Nconf  > $motif-sorted-dr.dat
rm -rf $devname*
rm $tmpname-*

echo '**************************************************************'
echo 'lrmsd $motif'
echo '**************************************************************'
nn=$1
list=$motif-clust1Ar.list
ligandr=`head -n 1 $list`
for i in `awk -v m=$motif '$2==m{print $1}' boundfrag.list`; do
    python2 $ATTRACTDIR/lrmsd.py $motif-sorted-dr.dat $ligandr frag$i\r.pdb --ens 2 $list --allatoms |awk '{print NR, $2}' > frag$i.lrmsd
done
}

#################################################################################

for motif in `cat motif.list`;do
  if [ ! -s $motif-sorted-dr.dat ] && [ ! -s $motif-20percent.dat ] ;then
      dock $motif $np
  fi
done

exit

a=`pwd|awk -F "/" '{print $NF}'`
cat /etc/hostname > dock.log
echo "../dock-motifs-systsearch.sh 8 $a >> dock.log 2> dock.err" | at now
