pypy $ATTRACTTOOLS/sort.py $1.dat > $1-sort.dat
$ATTRACTDIR/fix_receptor $1-sort.dat 2 --ens 0 $2 > $1-sort-fix.dat
$ATTRACTDIR/deredundant $1-sort-fix.dat 2 --ens 0 $2s > $1-dr.dat
