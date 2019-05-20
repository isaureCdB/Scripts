npz=$1
nfrag=$2
npy=$3

awk 'NR==1{i=$5;j=0}$5!=i{print j;j=0;i=$5}{j++}END{print j}' boundfrag/RNAr.pdb > boundfrag/nat

if [ ! -s  chains.txt ];then
    prepost_pattern=$4
    cat /dev/null > prepost
    for k in preatoms postatoms; do for j in `seq $nfrag`; do
        ls ${prepost_pattern}$k.npy >> prepost
    done;done

    make_chains_npz.py $npz 9999999 `cat prepost` \
     |awk 'NR>1{ for (i=2;i<=NF;i++) {printf "%s ", $i};printf "\n"}' > chains.txt
fi

if [ ! -s  rna.npy ];then
    echo '1' > /tmp/bi
    awk -v n=$nfrag '{ for (i=0;i<n+2;i++) {printf "6", $i}}' /tmp/bi > bi
    awk -v n=$nfrag '{ for (i=0;i<n;i++) {printf "0", $i}}' /tmp/bi > ba
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

if [ ! -s percent ];then
  percent_clash_chains.py chains_mindist_spacing$s $nfrag $s > percent
fi

for i in `awk 'NR>1{print $3}' percent |sort -u`; do
	awk -v i=$i 'BEGIN{m=0}$3==i&&$6>m{m=$6}END{print i"mer :", m}' percent
done
