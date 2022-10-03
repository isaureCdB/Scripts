#!/bin/bash
set -u -e

anchor1=$1  #ex: "out_attract_frag1" pour cibler "out_attract_frag1.dat"
anchor2=$2
frag1=$3
frag2=$4
motif1=`grep ' P ' refe/${frag1}-aa.pdb|awk '{print substr($4,length($4),1)}'| paste -sd ""` # "AAA" ou "frag1". C'est juste un template PDB
motif2=`grep ' P ' refe/${frag2}-aa.pdb|awk '{print substr($4,length($4),1)}'| paste -sd ""`

dump(){
  motif=$1
  anchor=$2
  frag=$3
  conf=`head -n 1 ${motif}-aa-clust1A.list`
  preatom=`cat $conf|wc -l|awk '{print $1}'`
  echo $preatom
  postatom="1"
  echo 'Dumping coordinates ' ${motif} ' ...'
  python $ATTRACTDIR/dump_coordinates.py $anchor.dat ${motif}-aa.pdb ${frag}-preatoms.npy 1 $preatom --ens 2 ../${motif}-aa-clust1A.list
  python $ATTRACTDIR/dump_coordinates.py $anchor.dat ${motif}-aa.pdb ${frag}-postatoms.npy 1 $postatom --ens 2 ../${motif}-aa-clust1A.list
  $ATTRACTDIR/lrmsd ${anchor}.dat ${motif}-aa.pdb refe/${frag}-aa.pdb --ens 2 ${motif}-aa-clust1A.list > ${frag}.lrmsd
}

#convertir les poses de docking du fragment ancre de .dat en .npy
dump $motif1 $anchor1 $frag1
dump $motif2 $anchor2 $frag2

distance=18
tolerance=0

python ../../scripts/script-assembly-real/combinatoric.py frag$frag1-preatoms.npy frag$frag2-postatoms.npy --distance $distance --tolerance $tolerance > frag$frag1-frag$frag2.combinable
pypy ../../scripts/script-assembly-real/analyze-possible.py frag$frag1-frag$frag2.combinable frag$frag1.lrmsd frag$frag2.lrmsd > frag$frag1-frag$frag2.combinable2
