awk -v m=$2 'BEGIN{j=0}($1=="MODEL" && j==1){exit}($1=="MODEL" && $2==m){j=1}j==1{print $0}' $1
