awk '$1=="ATOM"' $1 > /tmp/bi
renum-at-res.py /tmp/bi|egrep -v TER|egrep -v '[ 12][BCD][A-Z][A-Z][A-Z] ' > $1
j=`awk '$3=="CA"{print $4}' $1|sort -u`
for i in $j; do 
    sed -i 's/A'$i' / '$i' /' $1
done

