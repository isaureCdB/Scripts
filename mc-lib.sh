SCRIPTS=/data1/isaure/Scripts

set -u -e

receptorr=$1
ori=$2 #0.5
trans=$3 #1.0
nposes=$4 #list
np=$5 # nb of CPU

################################################
# You need to have, in the working directory:
################################################
# ------------------------------------------------
# a file "boundfrag.list" containing, for each of the bound fragments:
# its index (from 1) in the 1st column, and its sequence in 2nd column.
# ------------------------------------------------
# For each fragment of index x, a softlink to its reduces PDB file named frag{x}r.pdb
# and its all-atom PDB file named frag{x}-aa.pdb
# ------------------------------------------------
# for each sequence motif "m", a softlink to the lists:
# $m-clust1Ar.list : list of reduced fragments of motif m in the library (full path)
# $m-clust1A-aa.list : list of all-atom fragments of motif m in the library (full path)

mc(){
  frag=frag$1 #frag4
  m=`awk -v f=$1 '$1==f{print $2}' boundfrag.list`
  list=$m-clust1Ar.list
  listaa=$m-clust1A-aa.list
  Nconf=`cat $list|wc -l`
  start=mc3-$nposes-$frag
  echo $frag
  #if [ ! -s mc3-$nposes-$frag.dat ];then
  echo '**************************************************************'
  echo "Generate starting structures... $frag"
  echo '**************************************************************'

  python $ATTRACTTOOLS/fit.py `head -n 1 $list` $frag\r.pdb  --allatoms > $frag-ali.pdb
  python $ATTRACTTOOLS/fit.py `head -n 1 $listaa` $frag-aa.pdb  --allatoms > $frag-aa-ali.pdb ###

  $SCRIPTS/COM.py $receptorr |& awk '$1=="COM:"{print "#pivot 1 ", $2, $3, $4}' > xx$frag.dat
  $SCRIPTS/COM.py $frag-ali.pdb |& awk '$1=="COM:"{print "#pivot 2 ", $2, $3, $4}' >> xx$frag.dat
  awk 'NR > 1 && NR < 6' $ATTRACTDIR/../structure-single.dat >> xx$frag.dat
  python $ATTRACTTOOLS/euler.py $frag-ali.pdb  $frag\r.pdb >> xx$frag.dat

  python $ATTRACTTOOLS/monte.py xx$frag.dat --seed $RANDOM --ori $ori --trans $trans --fix-receptor --clone $nposes  > zero-$nposes-mc1-$frag.dat
  python $ATTRACTTOOLS/monte.py zero-$nposes-mc1-$frag.dat --seed $RANDOM --ori $ori --trans $trans --fix-receptor > zero-$nposes-mc2-$frag.dat
  python $ATTRACTTOOLS/monte.py zero-$nposes-mc2-$frag.dat --seed $RANDOM --ori $ori --trans $trans --fix-receptor > zero-$nposes-mc3-$frag.dat

  $ATTRACTDIR/collect zero-$nposes-mc1-$frag.dat /dev/null $frag-aa-ali.pdb > test1.pdb ###
  $ATTRACTDIR/collect zero-$nposes-mc2-$frag.dat /dev/null $frag-aa-ali.pdb > test2.pdb ###
  $ATTRACTDIR/collect zero-$nposes-mc3-$frag.dat /dev/null $frag-aa-ali.pdb > test3.pdb ###

  python $ATTRACTTOOLS/ensemblize.py zero-$nposes-mc3-$frag.dat $Nconf 2 all > $start.dat
  #fi

  ligandr=`head -n 1 $list`
  gridparams=" --grid 1 receptorgrid.gridheader"
  parals="--np $np --chunks $np"
  params="$ATTRACTDIR/../attract.par $receptorr $ligandr --fix-receptor --ens 2 $list $parals"

  echo '**************************************************************'
  echo "calculate receptorgrid grid $frag"
  echo '**************************************************************'
  awk '{print substr($0,58,2)}' $ligandr | sort -nu > receptorgrid.alphabet
  $ATTRACTDIR/make-grid-omp $receptorr $ATTRACTDIR/../attract.par 5.0 7.0 receptorgrid.gridheader  --shm --alphabet receptorgrid.alphabet
  echo '**************************************************************'
  echo 'scoring1'
  echo '**************************************************************'
  python2 $ATTRACTDIR/../protocols/attract.py $start.dat $params $gridparams --score --output $start.score
  python2 $ATTRACTTOOLS/fill-energies.py $start.dat $start.score > $start-scored.dat
  python2 $SCRIPTS/select-dat-perscore.py $start-scored.dat 1000 > $start-under1000.dat

  echo '**************************************************************'
  echo "docking $frag"
  echo '**************************************************************'
  python2 $ATTRACTDIR/../protocols/attract.py $start-under1000.dat $params $gridparams --vmax 100 --output $start-min100.dat
  $ATTRACTDIR/deredundant $start-min100.dat 2 --lim 0.05 --radgyr 6 --ens 0 $Nconf > $start-min100-dr005.dat

  echo '**************************************************************'
  echo "scoring2 $frag"
  echo '**************************************************************'
  python2 $ATTRACTDIR/../protocols/attract.py $start-min100-dr005.dat $params --score --rcut 50 --output $start-min100-dr005.score
  python2 $ATTRACTTOOLS/fill-energies.py $start-min100-dr005.dat $start-min100-dr005.score > $start-min100-dr005-scored.dat
  python2 $SCRIPTS/select-dat-perscore.py $start-min100-dr005-scored.dat 100 > $start-min100-dr005-scored-under100.dat
  python2 $ATTRACTTOOLS/sort.py $start-min100-dr005-scored-under100.dat > $start-min100-dr005-sorted.dat

  echo '**************************************************************'
  echo "deredundant $frag"
  echo '**************************************************************'
  $ATTRACTDIR/deredundant $start-min100-dr005-sorted.dat 2 --lim 0.1 --radgyr 6 --ens 0 $Nconf |\
    python $ATTRACTTOOLS/fill-deredundant.py /dev/stdin $start-min100-dr005-sorted.dat  > mc3-$nposes-$frag-min100-dr01.dat

  echo '**************************************************************'
  echo "lrmsd $frag"
  echo '**************************************************************'
  python2 $ATTRACTDIR/lrmsd.py mc3-$nposes-$frag-min100-dr01.dat $ligandr $frag\r.pdb --ens 2 $list --allatoms |awk '{print NR, $2}' > mc3-$nposes-$frag-min100-dr01.rmsd
  #awk '$2=="Energy"{print $3}' mc3-$nposes-$frag-min100-dr01.dat > mc3-$nposes-$frag-min100-dr01.ene
}
for f in `awk '{print $1}' boundfrag.list`; do
  mc $f
done
