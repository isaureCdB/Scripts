npz=$1
f1=$2
f2=$3
nfrag=`jq -n $f2-f1+1`

for m in `cat motif.list`; do
  n=`grep ATOM CUA/conf-1r.pdb|wc -l`
  dump_coordinates.py $m-e6.dat $m/conf-1r.pdb $m-e6.npy $m  `seq $m` --ens 2 $m-clust1A.list
done

if [ ! -s  chains.txt ];then
    make_chains_npz.py $npz 9999999 frag[$f1-$f2]-preatoms.npy frag[$f1-$f2]-postatoms.npy
     |awk 'NR>1{ for (i=2;i<=NF;i++) {printf "%s ", $i};printf "\n"}' > chains.txt
fi

if [ ! -s  rna.npy ];then
    echo '1' > /tmp/bi
    awk -v f1=$f1 -v f2=$f2 'NR>=f1&&NF<=f2{printf "%s", $1}}' /tmp/bi > nat
    awk -v n=$nfrag '{for (i=0;i<n;i++) {printf "%s", i}}}' /tmp/bi > motifs
    awk -v n=$nfrag '{ for (i=0;i<n;i++) {printf "0", $i}}' boundfrag.list > coor
    echo "chain2rna.py chains.txt $nfrag `cat bi` `cat ba` $npy  rna.npy"
    chain2rna.py chains.txt $nfrag `cat bi` `cat ba` $npy  rna.npy
fi

s=5
if [ "$nfrag" -eq 5 ];then s=4;fi

if [ ! -s  chains_mindist_spacing$s ];then
    cat /dev/null > coor
    for j in `seq $nfrag`; do
        echo $npy >> coor
    done
    mindist-frag-in-chains.py chains.txt $nfrag $s `cat coor` > chains_mindist_spacing$s
fi

if [ ! -s rna-$frag\mer.rmsd ];then
    rna-rmsd.sh $(($nfrag+2))
fi

percent_clash_chains.py chains_mindist_spacing$s $nfrag $s > percent

for i in `seq $nfrag $(($nfrag+2))` ; do
    echo "--------- $i-mer"
    awk -v i=$i '$3==i&&$4==5' percent |sort -nrk7 |head -n 5
done
