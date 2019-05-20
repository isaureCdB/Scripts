f=$1
c=$2

prepost(){
	g=$1
	cat /dev/null > prepost$g\frag
	for k in preatoms postatoms;do
		for i in `seq $g`; do
	  		echo  UUU-e6.$k.npy >> prepost$g\frag
	 	done
	done
}

cat /dev/null > npy$f\frag
for i in `seq $f`; do echo  UUU-e6.npy >> npy$f\frag;done

if [ ! -s UUU-e6-2frag-$c.npz ];then
	echo "connect 2frag"
	prepost 2
	connect-npz.py 2 $c 9999999999 1000 UUU-e6-2frag-$c.npz `cat prepost2frag`
fi

if [ ! -s UUU-e6-$f\frag-$c.npz ];then
	echo "connect $f frag"
	connect-homo-npz.py UUU-e6-2frag-$c.npz $f UUU-e6-$f\frag-$c.npz
fi
if [ ! -s UUU-e6-$f\frag-$c.chains ];then
	echo "make_chains_npz"
	prepost $f
	make_chains_npz.py UUU-e6-$f\frag-$c.npz 99999999 `cat prepost$f\frag` > UUU-e6-$f\frag-$c.chains
fi
if [ ! -s UUU-e6-$f\frag-$c.mindist ];then
	echo "mindist"
	mindist-frag-in-chains.py UUU-e6-$f\frag-$c.chains $f 5 `cat npy$f\frag` > UUU-e6-$f\frag-$c.mindist &
fi
if [ ! -s UUU-e6-$f\frag-$c.npy ];then
	echo "chain2rna"
	echo " " > x
	awk -v i=$f 'NR==1{for (j=0;j<i+2;j++) printf "%s", "6"; exit}' x > a
	awk -v i=$f 'NR==1{for (j=0;j<i;j++) printf "%s","0"; exit}' x > b
	chain2rna.py UUU-e6-$f\frag-$c.chains $f `cat a` `cat b` UUU-e6.npy UUU-e6-$f\frag-$c.npy
fi
if [ ! -s UUU-e6-$f\frag-$c.minlrmsd ];then
	echo "rmsdnpy"
	for i in `seq $((13-$f))`; do
		rmsdnpy.py UUU-e6-$f\frag-$c.npy ../boundfrag/n$i-$(($i+$f+1))\r.pdb > UUU-e6-$f\frag-$c.lrmsd-n$i-$(($i+$f+1)) &
	done
	wait
	paste UUU-e6-$f\frag-$c.lrmsd-n* | awk -v f=$f '{m=100}{for (i=2;i<=NF;i+=2){if ($i<m){m=$i; j=i/2}}}{print NR, m, "n"(j)"-"(f+j+1)}' > UUU-e6-$f\frag-$c.minlrmsd
fi
awk '$2<5.05' UUU-e6-$f\frag-$c.minlrmsd > UUU-e6-$f\frag-$c.minlrmsd-inf5
select-lines.py UUU-e6-$f\frag-$c.mindist UUU-e6-$f\frag-$c.minlrmsd-inf5 --noorder > UUU-e6-$f\frag-$c.mindist-inf5

exit
awk -v i=6 'BEGIN{j=0}$2<i||$3<i||$4<i||$5<i||$6<i{j++}END{print 100*j/NR}' UUU-e6-8frag-$c.mindist
awk -v i=6 'BEGIN{j=0}$2<i||$3<i||$4<i||$5<i||$6<i{j++}END{print 100*j/NR}' UUU-e6-8frag-$c.mindist-inf5

#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/chains.sh
