m1=$1 #min Nb of nucleotides
m2=$2 #max Nb of nucleotides

cat /dev/null > percent_clash_rnachain.txt
for s in `seq 5 $((m2-1))`;do
for m in `seq $m1 $m2`; do
for i in 4 5; do
    if [ ! -s chains_mindist_spacing$s-inf$i-$m\mer ];then
	    awk -v i=$i '$2<(i+0.05)' rna-$m\mer.rmsd > rna-$m\mer.rmsd-inf$i	
	    select-lines.py chains_mindist_spacing$s rna-$m\mer.rmsd-inf$i\
		            --dataorder > chains_mindist_spacing$s-inf$i-$m\mer
    fi
    if [ -s  chains_mindist_spacing$s-inf$i-$m\mer ];then
	for c in 1 2 3 4 5 6 8 10 ; do
		a=`awk -v j=$c '$3<j{n+=1}END{print 100*(NR-n)/NR}' chains_mindist_spacing$s-inf$i-$m\mer`
		b=`awk -v j=$c '$3<j{n+=1}END{print 100*(NR-n)/NR}' chains_mindist_spacing$s`
		inf5=`cat chains_mindist_spacing$s-inf$i-$m\mer|wc -l`
		tot=`cat chains_mindist_spacing$s|wc -l`
		p=`jq -n $inf5/$tot`
		d=`jq -n $a/$b`
		pp=`jq -n $d * $p`
		echo "$m-mer  inf$i  cutoff_$c : $p % => $pp %  ($d % increase)" >> percent_clash_rnachain.txt
    done
    fi
done
done
done
