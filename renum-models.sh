awk 'BEGIN{m=0}{if ($1=="MODEL") {m++;print "MODEL  " m} else  print $0}' $1
