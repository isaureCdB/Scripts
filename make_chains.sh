cat /dev/null > lrmsd$1\frag
cat /dev/null > prepost$1\frag
for k in preatoms postatoms; do
	for i in `seq $1`; do
		echo $k.npy >> prepost$1\frag
done;done
j=$2
for i in `seq $1`; do
	echo UUU-e6-clust1.lrmsd-frag$j >> lrmsd$1\frag
	j=$(($j+1))
done

make_chains_npz.py UUU-e6-clust1-$1\frag-2.0.npz 9999999 `cat prepost$1\frag` `cat lrmsd$1\frag` > UUU-e6-clust1-$1\frag_frag$2-$j\_2.0.chains
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/make_chains.sh
