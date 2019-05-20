BEGIN{j=1}  {if ($1==j) j++} { if ($1!=j)  {for ( k=j ; k < $1 ; k++ ) {print k }} ; {j=$1+1} }
