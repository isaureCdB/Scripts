npy=$1 #$m.npy
template=$2

maxens=`grep MAXENS /home/isaurec/attract/bin/max.h|awk '{print $5}'`
max=${maxens%;}
np=4

score(){
    mm=$1
    a=`cat $mm.list|wc -l`
    if [ ! -s ens-$a.dat ];then
        python $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/../structure-single.dat $a 2 all > ens-$a.dat
    fi
    python $ATTRACTDIR/../protocols/attract.py ens-$a.dat $ATTRACTTOOLS/../attract.par receptorr.pdb \
    $m-conf/conf-1.pdb --ens 2 $mm.list --score --rcut 50 --np $np --chunks $np --output $mm.score
    awk '$1=="Energy:"{i++; print i, $2}' $mm.score > $mm.energy
}

m=${npy%.npy}

npy2pdb.py $m.npy $template > $m.pdb
mkdir $m-conf
$ATTRACTTOOLS/splitmodel $m.pdb $m-conf/conf > $m.list

s=`cat $m.list|wc -l`

if [ $s -gt $max ];then
    split $m.list -l $max --additional-suffix="-$m.list"
    cat /dev/null > pre-$m.energy
    for list in `ls x??-$m.list`; do
        mm=${list%.list}
        score $mm
        echo $mm
        cat $mm.energy >> pre-$m.energy
        rm $mm.energy
    done
    awk '{print NR, $2}' pre-$m.energy > $m.energy
    rm pre-$m.energy
else
    score $m
fi
