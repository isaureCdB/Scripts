nalib=$1

nfrag=`cat boundfrag.list|wc -l`
receptorr=proteinr.pdb

for motif in `cat motif.list`; do
  ln -s $nalib/$motif
  ln -s $nalib/$motif-clust1Ar.list
done

set -u -e
###for j in `seq $nfrag`; do
for j in `seq 1`; do
  motif=`awk -v j=$j 'NR==j{print $2}' boundfrag.list`
  i=`awk -v j=$j 'NR==j{print $1}' boundfrag.list`
  $ATTRACTDIR/attract $ATTRACTDIR/../structure-single.dat  $ATTRACTDIR/../attract.par $receptorr boundfrag/frag$i\r.pdb --fix-receptor --vmax 100 > /tmp/frag$i.dat
  $ATTRACTDIR/attract /tmp/frag$i.dat  $ATTRACTDIR/../attract.par $receptorr boundfrag/frag$i\r.pdb  --score |awk '$1=="Energy:"{print $2}' > boundfrag/frag$i-min100.score
  python2 $ATTRACTDIR/lrmsd.py /tmp/frag$i.dat boundfrag/frag$i\r.pdb boundfrag/frag$i\r.pdb --allatoms > boundfrag/frag$i-min100.rmsd
  $ATTRACTDIR/attract $ATTRACTDIR/../structure-single.dat  $ATTRACTDIR/../attract.par $receptorr boundfrag/frag$i\r.pdb  --score |awk '$1=="Energy:"{print $2}' > boundfrag/frag$i.score
  python2 $ATTRACTTOOLS/fit-multi.py boundfrag/frag$i\r.pdb $motif-clust1Ar.list --allatoms --rmsd |awk '{print NR, $1}'> boundfrag/frag$i\r.rmsd
done
