awk 'BEGIN{m=1;n=0}{n+=(NF-3); for (i=4;i<=NF;i++) if ($i>m) m=$i }END{print m, "among", n}' $1
