rec=$1
lig=$2

nlig=`cat $lig|wc -l`
nrec=`cat $rec|wc -l`

for i in `seq $nlig`; do
	awk -v i=$i 'NR==i' $lig > /tmp/ligbead$i.pdb
done

for i in `seq $nrec`; do
	awk -v i=$i 'NR==i' $rec > /tmp/recbead$i.pdb
done

	
for i in `seq $nrec`; do
	for j in `seq $nlig`; do
		$ATTRACTDIR/attract $ATTRACTDIR/../structure-single.dat $ATTRACTDIR/../attract.par /tmp/recbead$i.pdb /tmp/ligbead$j.pdb |awk -v i=$i j=$j '$2=="Energy:"{print i, j, $3}'
	done
done
