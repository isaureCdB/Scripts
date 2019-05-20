BEGIN{j=1} $1==j{print $0; j++} $1!=j{for ( k=j ; k < $1 ; k++ ) {print k, "None"; print $0}} {j=$1+1}
