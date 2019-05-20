#!/bin/bash -i
set -u -e
awk '$1=="#pivot"||$1=="#centered"' $1.dat > $1.header
awk 'NR<5||(NF==7 && substr($1, 1, 1)!="#")' $1.dat > $1.txt
awk '$2=="Energy:"{print $3}' $1.dat > $1.ene
bzip2 $1.txt $1.ene
#rm $1.dat
