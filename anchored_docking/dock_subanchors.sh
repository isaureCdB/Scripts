set -e -u

frag=$1
mode=$2
motif=`grep GP1 refe/${frag}r.pdb|awk '{print substr($4,length($4),1)}'| paste -sd ""`
name="dock-${frag}"

#export ATTRACTDIR='/home/ibeauchene/frag-attract/bin'
#export ATTRACTTOOLS='/home/ibeauchene/frag-attract/tools'

# The docking is made on an ensemble of protein-anchor complexes.
# anchor = one of the cluster-center of the docking poses of the previous fragment
# To create the list, use prep-subanchors.sh
listprot="proteincr-subanchor-${frag}-${mode}.list"

list="$motif-clust1A.list"
ens=`cat $list | wc -l`
ensprot=`cat $listprot | wc -l`
parals1='--np 24 --chunks 8' ###
params="$ATTRACTDIR/../attract.par subanchors/proteincr-subanchor-${frag}-${mode}-1.pdb `head -n 1 $list` --ens 2 $list --ens 1 $listprot  --fix-receptor --rest ${frag}-$mode.rest "

# As the starting dat files with ensembles cn be quite long to create, I have a env viariable for a directory
# were I store all of them. So if I need a dat with same Nposes and ensemble sizes as previously, I will not recreate it
# "Nlige3" = 1000 poses
if [ ! -f $RANDSEARCH/randsearch-Nlige3-$ensprot.dat ]; then
  pypy $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/randsearch-Nlig2-3e4.dat $ensprot 1 all > $ATTRACTTOOLS/randsearch-Nlige3-$ensprot.dat
fi
if [ ! -f ../randsearch-3e7-${motif}.dat ]; then
  pypy $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/randsearch-Nlige3-$ensprot.dat $ens 2 random > ../randsearch-3e7-${motif}.dat
fi

#cp on shm to gain execution time
# !!! Do NOT FORGET to delete it afterward !!!
cp randsearch-3e7-${motif}.dat /dev/shm/randsearch-3e7-${motif}.dat
randsearch=/dev/shm/randsearch-3e7-${motif}.dat

python $ATTRACTDIR/../protocols/attract.py $randsearch $params $parals1 --ghost --output ${name}-ghost.dat

$ATTRACTDIR/shm-clean
awk '{print substr($0, 58,2)}' refe/${frag}r.pdb | sort -u > ${motif}r.alphabet
$ATTRACTDIR/make-grid-omp subanchors/proteincr-subanchor-${frag}-${mode}-1.pdb $ATTRACTDIR/../attract.par 10 12 proteincr-subanchor-${frag}-${mode}.gridheader --shm --alphabet ${motif}r.alphabet
gridparams="--grid 1 proteincr-subanchor-${frag}-${mode}.gridheader"
parals2='--np 8 --chunks 8' ###

python $ATTRACTDIR/../protocols/attract.py ${name}-ghost.dat $params $gridparams $parals2 --output ${name}.dat

pypy $SCRIPTS/select-per-fragment.py ${name}.dat 0.2 | python $ATTRACTTOOLS/sort.py /dev/stdin | \
  $ATTRACTDIR/fix_receptor /dev/stdin 2 --ens $ensprot $ens  | \
  $ATTRACTDIR/deredundant /dev/stdin 2 --ens $ensprot $ens | \
  python $ATTRACTTOOLS/de-ensemblize.py /dev/stdin 1 > ${name}-top0.2-dr.dat

python $ATTRACTDIR/lrmsd.py ${name}-top0.2-dr.dat `head -n 1 ${motif}-aa-clust1A.list` refe/${frag}-aa.pdb --allatoms --ens 2 ${motif}-aa-clust1A.list | \
  awk '{print NR,$2}'|sort -nk2 > ${name}-top0.2-dr.lrmsd-sorted

rm -f $randsearch
$ATTRACTDIR/shm-clean
