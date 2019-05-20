m=$1
tot=$2
mkdir ${m}mer-rmsd

n=$(echo $tot - $m + 1 | bc)

echo $m $tot $n
#if false; then
	if [ $m -eq $tot ];then
		ln -s rna.npy  rna_${m}mer_1.npy
	fi	
	for i in `seq $n`; do
		if [ ! -s rna_${m}mer_$i.npy ];then
			select-atom-npy.py rna.npy atom-selections/sel-n$i-$(($i+$m-1)) rna_${m}mer_$i.npy
		fi
		for j in `tail -n 5 boundfrag/${m}-mer.list`; do
			if [ ! -s ${m}mer-rmsd/rna_${m}mer_$i\_bound$j.rmsd ];then
				rmsdnpy.py rna_${m}mer_$i.npy boundfrag/$j\r.pdb > ${m}mer-rmsd/rna_${m}mer_$i\_bound$j.rmsd
			fi
		done
	done
#fi

paste ${m}mer-rmsd/rna_${m}mer_?_bound*.rmsd | awk  '{m=100; for (i=2;i<=NF;i+=2) if ($i<m) m=$i ; print NR, m}' > rna-${m}mer.rmsd

awk '$2<5.05{i++}END{print i, 100*i/NR}' rna-${m}mer.rmsd
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/rna-rmsd.sh
