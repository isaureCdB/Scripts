awk '{print NR, $1}' $1 |sort -nk2 > $1-sorted
