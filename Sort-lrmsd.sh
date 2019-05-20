awk '{print NR, $2}' $1 |sort -nk2 > $1-sorted
