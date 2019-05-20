npz=$1
nfrag=$2
npy=$3

#dump_coordinates.py $m-e6.dat $m/conf-1r.pdb $m-e6.npy $n `seq $n` --ens 2 $m-clust1A.list
ln -s ../../../boundfrag

if [ ! -s  chains.txt ];then
  cat /dev/null > coor
  for k in preatons postatoms; do
    for i in `seq $nfrag`; do
      ls $k.npy >> coor
    done
  done
  make_chains_npz.py $npz 1000000 `cat coor` \
    | awk 'NR>1{ for (i=2;i<=NF;i++) {printf "%s ", $i};printf "\n"}' > chains.txt
fi

cat /dev/null > coor
for i in `seq $nfrag`; do ls $npy >> coor; done

if [ ! -s  rna.npy ];then
    echo "1" > /tmp/bi
    awk 'NR==1{i=$5;j=0}$5!=i{print j;j=0;i=$5}{j++}END{print j}' boundfrag/RNAr.pdb > boundfrag/nat
    awk -v n=$nfrag 'NR==1{for (i=0;i<=n+1;i++) {printf "%s", $1}}' boundfrag/nat  > nat
    awk -v n=$nfrag '{for (i=0;i<n;i++) {printf "0"}}' /tmp/bi > motifs
    #awk -v n=$nfrag '{ for (i=0;i<n;i++) {printf "0", $i}}' boundfrag.list > coor
    echo "chain2rna.py"
    chain2rna.py chains.txt $nfrag `cat nat` `cat motifs` $npy rna.npy
fi

s=5
if [ "$nfrag" -eq 5 ];then s=4;fi

if [ ! -s  chains_mindist_spacing$s ];then
    mindist-frag-in-chains.py chains.txt $nfrag $s `cat coor` > chains_mindist_spacing$s
fi

if [ ! -s rna-$frag\mer.rmsd ];then
    rna-rmsd.sh $(($nfrag+2))
fi

percent_clash_chains.py chains_mindist_spacing$s $nfrag $s > percent

for i in `seq $nfrag $(($nfrag+2))` ; do
    echo "--------------------------------- $i-mer"
    awk -v i=$i '$3==i&&$4==5' percent |sort -nrk7 |head -n 5
done
