rec=$1
lig=$2

nlig=`cat $lig|wc -l`
nrec=`cat $rec|wc -l`

x=$RANDOM

$SCRIPTS/splitlines.py $rec /tmp/rec-$x- > rec-$x.list
$SCRIPTS/splitlines.py $lig /tmp/lig-$x- > lig-$x.list

$ATTRACTTOOLS/ensemblize.py $ATTRACTDIR/../structure-single.dat $nlig 2 all > lig.dat

for i in `seq $nrec`; do

	#for coarse-grain:
	$ATTRACTDIR/attract lig.dat $ATTRACTDIR/../attract.par /tmp/rec-$x-$i /tmp/lig-$x-1.pdb --ens 2 lig-$x.list > /tmp/$x.scores

	#for all atom:
	#$ATTRACTDIR/attract lig.dat $ATTRACTDIR/../allatoms/allatom.par /tmp/rec-$x-$i /tmp/lig-$x-1.pdb --ens 2 lig-$x.list > /tmp/$x.scores

	awk -v i=$i 'BEGIN{j=0}$2=="Energy:"{j+=1; print i, j, $3}' /tmp/$x.scores
done
