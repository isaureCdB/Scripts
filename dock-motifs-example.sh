#!/bin/bash -i

trap "kill -- -$BASHPID; $ATTRACTDIR/shm-clean" ERR EXIT
$ATTRACTDIR/shm-clean

# convert into coarse-grained representation.
# this creates receptorr.pdb (additional r for "reduced")
python $ATTRACTTOOLS/../allatom/aareduce.py receptor.pdb --heavy
python $ATTRACTTOOLS/reduce.py receptor-aa.pdb

receptorr=receptor-aar.pdb
receptoraa=receptor-aa.pdb

#TODO: adjust nb of starting positions to the size of the receptor (radgyr) ?

#TODO: Nstart = 30 for testing. Change to 30000000 for real docking
### You might want to lower that number if you have less than 32GM memory,
# and increase if you have more than 64GB.
#Nstart=30000000
Nstart=30

#######################################################
# For randsearch
#######################################################
# Create one $RANDSEARCH directory common for the whole benchmark,
#  where you put the files containing the starting positions on a shpere,
# so you don't have to recalculate at each docking
########################################################
# For systsearch
########################################################
# The set of starting positions has to be created for each protein,
# since the positions depend on the protein shape.
# But it does not have to be recreated for each motif.
# Create it with the largest GGG conformer, as the distance from protein to points
# depend on the ligand radius, and we do not want it too close to the protein,
# to avoid clashes

# create a $RANDSEARCH directory where you put the files containing the
# starting position, so you don't have to recalculate at each docking.
if [ ! -s $RANDSEARCH//randsearch-$Nstart.dat ];then
    pypy $ATTRACTTOOLS/randsearch.py 2 $Nstart --fix-receptor > $RANDSEARCH//randsearch-$Nstart.dat
fi

dock(){
  set -u -e
  motif=$1 # trinucl sequence
  np=$2 # nb of CPU
  list="$LIBRARY/$m-clust1A.list" # list of recduced fragments (full path)
  listaa="$LIBRARY/$m-clust1A-aa.list" # list of all-atom fragments (full path)
  ligandr=`head -n 1 $list`
  ligandaa=`head -n 1 $listaa`
  Nconf=`cat $list|wc -l`
  ln -s $LIBRARY/$m

  gridparams=" --grid 1 receptorgrid.gridheader"
  parals="--np $np --chunks $np"

  #!!! TODO: remove gravity for systsearch!!!
  params="$ATTRACTDIR/../attract.par $receptorr $ligandr --fix-receptor --ens 2 $list --gravity 2 $gridparams"

  scoreparams="$ATTRACTDIR/../attract.par $receptorr $ligandr --score --fix-receptor --ens 2 $list --rcut 50 $parals"

  #$paramsaa="$ATTRACTDIR/../allatom/allatom.par $receptor $ligandaa --fix-receptor --ens 2 $listaa"
  #scoreparamsaa="$ATTRACTDIR/../allatom/allatom.par $receptor $ligandaa --score --fix-receptor --ens 2 $listaa"

  echo '**************************************************************'
  echo 'calculate receptorgrid grid'
  echo '**************************************************************'
  awk '{print substr($0,58,2)}' $ligandr | sort -nu > receptorgrid.alphabet
  $ATTRACTDIR/make-grid-omp $receptorr $ATTRACTDIR/../attract.par 5.0 7.0 receptorgrid.gridheader  --shm --alphabet receptorgrid.alphabet

  echo '**************************************************************'
  echo 'Generate starting structures...'
  echo '**************************************************************'
  # distribute all conformers of the library to each starting position
  # = Create a set of random starting orientations for all conformers at each position,
  # only if it was not yet created for that number of conformers
  if [ ! -s $RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat ];then
      pypy $ATTRACTTOOLS/ensemblize.py $RANDSEARCH/randsearch-$Nstart.dat $Nconf 2 random > $RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat
  fi

  start=$RANDSEARCH/randsearch-$Nstart-ens-$Nconf.dat

  ##TODO: test systsearch

  echo '**************************************************************'
  echo 'docking'
  echo '**************************************************************'
  python $ATTRACTDIR/../protocols/attract.py $start --vmax 100 --output $m.dat

  ##TODO: For randsearch, test refinement without gravity
  #refine="$ATTRACTDIR/../attract.par $receptorr $ligandr --fix-receptor --ens 2 $list 2 $gridparams"
  #python $ATTRACTDIR/../protocols/attract.py $m.dat --vmax 100 --refine --output $m-refine.dat

  ###TODO: test deredundant before scoring and sorting
  # default limit for deredundant is 0.05A.
  # For a 21 beads ligand, if only 1 bead deviates (e.g. phos), it can deviate by 0.23A.
  #                        if only 3 beads deviate equaly (e.g. base) => 0.13A

  # $ATTRACTDIR/deredundant $m.dat 2 --ens 0 $Nconf --radgyr 9 > $m-dr.dat


  echo '**************************************************************'
  echo 'scoring'
  echo '**************************************************************'
  python $ATTRACTDIR/../protocols/attract.py $m.dat $scoreparams --output $m.score

  # remove the cashed grid
  $ATTRACTDIR/shm-clean

  ### TODO: test all-atom redocking and scoring
  # python $ATTRACTDIR/../protocols/attract.py $m.dat $paramsaa --vmax 100 --output $m-aa.dat
  # python $ATTRACTDIR/../protocols/attract.py $m-aa.dat $scoreparamsaa --vmax 100 --output $m-aa.score

  ### TODO: test all-atom dockign with larger library

  echo '**************************************************************'
  echo 'processing results'
  echo '**************************************************************'
  ### TODO: test quick way to select top-scored poses before sorting (optional)
  #python3 $SCRIPTS/select-dat-perrank.py $m.dat --score $m.score --percent 30 --outpscore $m-30pc.score > $m-30pc.dat

  python $ATTRACTTOOLS/fill-energies.py $m.dat $m.score > $m-scored.dat

  python $ATTRACTTOOLS/sort.py $m-scored.dat > $m-sorted.dat

  $ATTRACTDIR/fix_receptor $m-sorted.dat 2 --ens 0 $Nconf | python $ATTRACTTOOLS/fill.py /dev/stdin $m-sorted.dat > $m-sorted.dat-fixre

  $ATTRACTDIR/deredundant $m-sorted.dat-fixre 2 --ens 0 $Nconf --radgyr 9 | python $ATTRACTTOOLS/fill-deredundant.py /dev/stdin $m-sorted.dat-fixre > $m-sorted-dr.dat

  #$ATTRACTTOOLS/top $m-sorted-dr.dat 10000000 > $m-e7.dat

  echo '**************************************************************'
  echo 'compute RMSD'
  echo '**************************************************************'
  # compute deviation of each pose toward the bound fragment
  # TODO: cut the reduced bound RNA into fragments to be stored as boundfrag/frag${i}r.pdb
  # by running extractfrag.sh
  for i in `awk -v m=$m '$2==m{print $1}' boundfrag.list`; do
      python $ATTRACTDIR/lrmsd.py $m-sorted-dr.dat $ligandr boundfrag/frag$i\r.pdb --ens 2 $list --allatoms |awk '{print NR, $2}' > $m-sorted-dr-frag$i.lrmsd
  done
  set -u +e
}

np=32 # Number of CPU
dir=`pwd`

for complex in complexes.list; do
    cd $complex
    # motif.list gives the non-redundant list of all sequence motifs in the RNA sequence,
    # one per line. For a poly-U, it will contain only one line with UUU
    for m in `cat motif.list`;do
      dock $m $np > dock-$m.log 2> dock-$m.err
    done
    cd $dir
done
