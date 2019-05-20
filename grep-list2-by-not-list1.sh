pat=`python -c "print open('"$1"').read().replace('\n', '|')[:-1]"`
egrep -v "$pat" $2
