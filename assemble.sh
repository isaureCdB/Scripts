# assemble homo-polymer

json=$1 # ex: UUU-5-5A.json
frag1=$2 # index of 1st fragment in sequence
frag2=$3 # index of last fragment in sequence
cutoff=$4
meanrk=$5

l="frag["$frag1"-"$frag2"].rmsd"
a="frag["$frag1"-"$frag2"]-preatoms.npy"
b="frag["$frag1"-"$frag2"]-postatoms.npy"

name=$json-frag$frag1-$frag2
python make_chains.py $json $meanrk $a $b $l > $name.chains

nfrags=$(($frag2-$frag1+1))
for i in `seq $nfrags`; do
    f=$(($frag1+$i-1))
    awk -v i=$i '$1=="#indices"{print $(4+i)}' $name.chains |uniq|sort -nk1|uniq > /tmp/$name.fragment$f;
    python select-lines.py frag$f.rmsd /tmp/$name.fragment$f |paste /tmp/$name.fragment$f /dev/stdin > $name.fragment$f
done

