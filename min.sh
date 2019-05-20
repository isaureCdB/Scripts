awk 'BEGIN{m=100}$2<m{m=$2;j=NR}END{print NR, m}' $1
