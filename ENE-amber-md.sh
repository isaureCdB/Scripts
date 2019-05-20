grep Etot $1.out|awk '{print $3}'|head -n -2 > $1.ene
