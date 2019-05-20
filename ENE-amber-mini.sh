grep -A1 ENERGY $1.out|egrep -v '\-\-|ENE' |awk '{print $2}'> $1.ene
