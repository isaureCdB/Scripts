x=$RANDOM
awk '{for (i=2;i<=NF;i++){printf "%.1f ", $i}}{printf "\n"}' $1 > /tmp/bi-$x
mv -f /tmp/bi-$x $i
