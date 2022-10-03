#####  USAGE : dock_2anchors.sh AAA 10
#pypy $ATTRACTTOOLS/randsearch.py 2 100 12345 --fast --fix-receptor --radius 100 > randsearch.dat

motif=$1
anchor=$2

$ATTRACTDIR/shm-clean
awk '{print substr($0, 58,2)}' ${motif}r.pdb | sort -u > ${motif}r.alphabet
$ATTRACTDIR/make-grid-omp proteincr-2anchors.pdb $ATTRACTDIR/../parameters_all_rna.par 10 12 proteincr-2anchors-${motif}.gridheader --shm --alphabet ${motif}r.alphabet
$ATTRACTDIR/shm-grid proteincr-2anchors-${motif}.grid proteincr-2anchors-${motif}-$anchor.gridheader
list="$motif-clust1A.list"
ens=`cat $list | wc -l`

pypy $ATTRACTTOOLS/ensemblize.py randsearch.dat $ens 2 all > randsearch-ensemble-${motif}.dat

# In a first docking step, the fragment is orientated toward the anchor via the restraints.
# The force-field is disabled ("ghost" option) as well as tramnslations ("only-rot" option)
paramsrot="$ATTRACTDIR/../parameters_all_rna.par proteincr-2anchors.pdb ${motif}r.pdb --ens 2 $list --ghost --rest ${anchor}.rest --only-rot"


params="$ATTRACTDIR/../parameters_all_rna.par proteincr-2anchors.pdb ${motif}r.pdb --ens 2 $list --grid 1 proteincr-2anchors-${motif}-$anchor.gridheader --rest ${anchor}.rest --fix-receptor --gravity 1"
#paramscore="$ATTRACTDIR/../parameters_all_rna.par proteincr-2anchors.pdb ../${motif}r.pdb --ens 2 $list --grid 1 proteincr-2anchors-${motif}.gridheader --rest ${anchor}.rest --fix-receptor --gravity 1"
parals='--np 12 --chunks 4'

python $ATTRACTDIR/../protocols/attract.py randsearch-ensemble-${motif}.dat $paramsrot $parals --output dock-${motif}-${anchor}-rot.dat
python $ATTRACTDIR/../protocols/attract.py dock-${motif}-${anchor}-rot.dat $params $parals --output dock-${motif}-${anchor}.dat
pypy $ATTRACTTOOLS/sort.py dock-${motif}-${anchor}.dat > dock-${motif}-${anchor}-sort.dat
$ATTRACTDIR/fix_receptor dock-${motif}-${anchor}-sort.dat 2 --ens 0 $ens  > dock-${motif}-${anchor}-sort-fix.dat
$ATTRACTDIR/deredundant dock-${motif}-${anchor}-sort-fix.dat 2 --ens 0 $ens > dock-${motif}-${anchor}-dr.dat

#Select the 20% top-ranked poses
n=`grep SEED  dock-${motif}-${anchor}-dr.dat|wc -l`
top20=$(($n/5))
echo "top 20% = $top20"
Top dock-${motif}-${anchor}-dr.dat $top20 > dock-${motif}-${anchor}-dr-top0.2.dat
lrmsd dock-${motif}-${anchor}-dr-top0.2.dat ../$motif/conf-1.pdb frag${frag}.pdb --ens 2 ${motif}-all-clust1A.list > dock-${motif}-${anchor}-dr-top0.2.lrmsd
