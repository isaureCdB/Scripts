#!/bin/bash -i

trap "kill -- -$BASHPID; $ATTRACTDIR/shm-clean" ERR EXIT
$ATTRACTDIR/shm-clean

# convert into coarse-grained representation.
# this creates receptorr.pdb (additional r for "reduced")
python $ATTRACTTOOLS/reduce.py receptor.pdb

receptorr=receptorr.pdb

#TODO: adjust nb of starting positions to the size of the receptor (radgyr)
### !!! Nstart = 30 for testing. Change to 30000000 for real docking
### (you might want to lower that number if you have less than 32GM memory)
#Nstart=30000000
Nstart=30

# create a $RANDSEARCH directory where you put the files containing the
# starting position, so you don't have to recalculate at each docking.
if [ ! -s $RANDSEARCH//randsearch-$Nstart.dat ];then
    pypy $ATTRACTTOOLS/randsearch.py 2 $Nstart --fix-receptor > $RANDSEARCH//randsearch-$Nstart.dat
fi

dock(){
  set -u -e
  motif=$1 # trinucl sequence
  np=$2 # nb of CPU
  list="$LIBRARY/$motif-clust1A.list" # list of recduced fragments (full path)
  listaa="$LIBRARY/$motif-clust1A-aa.list" # list of all-atom fragments (full path)
  ligandr=`head -n 1 $list`
  ligandaa=`head -n 1 $listaa`
  Nconf=`cat $list|wc -l`
  ln -s $LIBRARY/$motif

  gridparams=" --grid 1 receptorgrid.gridheader"
  parals="--np $np --chunks $np"
  params="$ATTRACTDIR/../attract.par $receptorr $ligandr --fix-receptor --ens 2 $list --gravity 2 $gridparams"
  scoreparams="$ATTRACTDIR/../attract.par $receptorr $ligandr --score --fix-receptor --ens 2 $list --rcut 50 $parals"

  echo '**************************************************************'
  echo 'calculate receptorgrid grid'
  echo '**************************************************************'
  awk '{print substr($0,58,2)}' $ligandr | sort -nu > receptorgrid.alphabet
  $ATTRACTDIR/make-grid-omp $receptorr $ATTRACTDIR/../attract.par 5.0 7.0 receptorgrid.gridheader  --shm --alphabet receptorgrid.alphabet

  echo '**************************************************************'
  echo 'Generate starting structures...'
  echo '**************************************************************'
  # distribute all conformers of the library to each starting position
  if [ ! -s $RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat ];then
      pypy $ATTRACTTOOLS/ensemblize.py $RANDSEARCH/randsearch-$Nstart.dat $Nconf 2 random > $RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat
  fi

  start=$RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat

  echo '**************************************************************'
  echo 'docking'
  echo '**************************************************************'
  python $ATTRACTDIR/../protocols/attract.py $start $params --vmax 100 --output $motif.dat

  echo '**************************************************************'
  echo 'scoring'
  echo '**************************************************************'
  python $ATTRACTDIR/../protocols/attract.py $motif.dat $scoreparams --output $motif.score

  # remove the cashed grid
  $ATTRACTDIR/shm-clean

  echo '**************************************************************'
  echo 'processing results'
  echo '**************************************************************'
  python $ATTRACTTOOLS/fill-energies.py $motif.dat $motif.score > /tmp/$motif-scored.dat

  python $ATTRACTTOOLS/sort.py /tmp/$motif-scored.dat > /tmp/$motif-sorted.dat

  $ATTRACTDIR/fix_receptor /tmp/$motif-sorted.dat 2 --ens 0 $Nconf | python $ATTRACTTOOLS/fill.py /dev/stdin /tmp/$motif-sorted.dat > /tmp/$motif-sorted.dat-fixre

  $ATTRACTDIR/deredundant /tmp/$motif-sorted.dat-fixre 2 --ens 0 $Nconf | python $ATTRACTTOOLS/fill-deredundant.py /dev/stdin /tmp/$motif-sorted.dat-fixre > $motif-sorted-dr.dat
  rm $motif.dat $motif.score

  $ATTRACTTOOLS/top $motif-sorted-dr.dat 10000000 > $motif-e7.dat

  echo '**************************************************************'
  echo 'compute RMSD'
  echo '**************************************************************'
  # compute deviation of each pose toward the bound fragment
  # TODO: cut the reduced bound RNA into fragments to be stored as boundfrag/frag${i}r.pdb
  # by running extractfrag.sh
  for i in `awk -v m=$motif '$2==m{print $1}' boundfrag.list`; do
      python $ATTRACTDIR/lrmsd.py $motif-e7.dat $ligandr boundfrag/frag$i\r.pdb --ens 2 $list --allatoms |awk '{print NR, $2}' > frag$i.lrmsd
  done
  set -u +e
}

for i in `cat motif.list`;do  #motif.list is created by extractfrag.sh
  dock $i 16
done
