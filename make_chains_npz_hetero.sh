npz=$1
f1=$2
f2=$3
n1=$f1
n2=$(($f2+2))
nfrag=`jq -n $f2-$f1+1`
name=${npz%*.npz}

if false ;then
  for m in `cat motif.list`; do
    if [ ! -s $m.npy ];then
      n=`grep ATOM $m/conf-1r.pdb|wc -l`
      dump_coordinates.py $m-e6.dat $m/conf-1r.pdb $m-e6.npy $n `seq $n` --ens 2 $m-clust1A.list
    fi
  done
fi

ln -s ../../boundfrag

if [ ! -s  ${name}_chains.txt ];then
  echo "make_chains_npz"
  make_chains_npz.py $npz 1000000 frag[$f1-$f2]-preatoms.npy frag[$f1-$f2]-postatoms.npy \
  | awk 'NR>1{ for (i=2;i<=NF;i++) {printf "%s ", $i};printf "\n"}' > ${name}_chains.txt
fi

if [ ! -s  ${name}_rna.npy ];then
    echo "1" > /tmp/bi
    awk 'NR==1{i=$5;j=0}$5!=i{print j;j=0;i=$5}{j++}END{print j}' boundfrag/RNAr.pdb > boundfrag/nat
    awk -v n1=$n1 -v n2=$n2 'NR>=n1&&NR<=n2{printf "%s", $1}' boundfrag/nat  > nat
    awk -v n=$nfrag '{for (i=0;i<n;i++) {printf "%s", i}}' /tmp/bi > motifs
    #awk -v n=$nfrag '{ for (i=0;i<n;i++) {printf "0", $i}}' boundfrag.list > coor
    echo "chain2rna.py "
    chain2rna.py ${name}_chains.txt $nfrag `cat nat` `cat motifs` frag[$f1-$f2].npy  ${name}_rna.npy
fi

s=5
if [ "$nfrag" -eq 5 ];then s=4;fi

if [ ! -s  ${name}_chains_mindist_spacing$s ];then
    mindist-frag-in-chains.py ${name}_chains.txt $nfrag $s frag[$f1-$f2].npy > ${name}_chains_mindist_spacing$s
fi

percent(){
  n1=$1;   n2=$2
  if [ ! -s ${name}_rna-$n1-$n2.lrmsd ];then
    awk -v n1=$n1 -v n2=$n2 'BEGIN{i=0}$5>=n1&&$5<=n2{i++; print i}' boundfrag/RNAr.pdb > /tmp/sel-n$n1-$n2
    awk -v n1=$n1 -v n2=$n2 '$5>=n1&&$5<=n2' boundfrag/RNAr.pdb > /tmp/n$n1-$n2
    select-atom-npy.py ${name}_rna.npy /tmp/sel-n$n1-$n2 ${name}_rna-$n1-$n2.npy
    rmsdnpy.py ${name}_rna-$n1-$n2.npy /tmp/n$n1-$n2 > ${name}_rna-$n1-$n2.lrmsd
  fi
  percent_clash_chains_hetero.py ${name}_rna-$n1-$n2.lrmsd ${name}_chains_mindist_spacing$s $nfrag $s > ${name}_percent-n$n1-$n2
  echo "-------------- ${name}_percent-n$n1-$n2"
  sort -nrk6 ${name}_percent-n$n1-$n2 |head -n 5
}

percent $f1 $n2
percent $f1 $(($n2-1))
percent $(($f1+1)) $n2
