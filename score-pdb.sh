rec=$1
lig=$2

$ATTRACTDIR/attract $ATTRACTDIR/../structure-single.dat $ATTRACTDIR/../attract.par $1 $2|awk '$2=="Energy:"{print $3}'
