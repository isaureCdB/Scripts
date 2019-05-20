awk '$1=="ATOM" && $3=="CA"' $1 > /tmp/bi

awk -v a=$2 -v b=$3 -v c=$4 -v d=$5 'BEGING{i=0}
    i==3{if ($4==d) print substr($0, 22,6)-3; else i=0}
    i==2{if ($4==c) i=3; else i=0}
    i==1{if ($4==b) i=2; else i=0}
    i==0{if ($4==a) i=1}' /tmp/bi
