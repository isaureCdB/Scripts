d=/home/isaurec/projets/ssRNA/chinmay/sel5e5/
ln -s $d/../receptorr.pdb
ln -s $d/../receptorr.pdb
ln -s /home/isaurec/projets/ssRNA/noanchors/1b7f/docking5/UUU-5e5.npy
natom="6 6 6 6 6 6 6 6"
motifs="0 0 0 0 0 0"

evaluate(){
    a=$1
    echo "------------------ inf5 $a"
    awk '$2<5.05{i++}NR==10||NR==20||NR==100||NR==1000{print "top"NR": ", i}\
    END{print "all-"NR": ",i}' $a
}

chain2rna.py chains.txt "`echo $natom`" "`echo $motifs`" UUU-5e5.npy rna.npy
noclash-chains.py rna.npy 3 3 $natom > rna-noclash


a=`cat chains.txt|wc -l`
b=`cat rna-noclash|wc -l`
echo "$a uniq chains, $b not clashing"
for i in `ls $d/n*r.pdb`; do ln -s $i ; done
rmsdnpy.py rna.npy n3-10r.pdb > rna.rmsd

rmsdnpy.py rna.npy n3-9r.pdb `seq 42` > n3-9r-1.rmsd
rmsdnpy.py rna.npy n3-9r.pdb `seq 7 48` > n3-9r-2.rmsd
rmsdnpy.py rna.npy n4-10r.pdb `seq 42` > n4-10r-1.rmsd
rmsdnpy.py rna.npy n4-10r.pdb `seq 7 48` > n4-10r-2.rmsd
paste n3-9r-?.rmsd n3-10r-?.rmsd | awk '{m=$4}$2<$4{m=$2}$6<m{m=$6}$8<m{m=$8}{print NR, m}' > rna.7mer-rmsd
select-lines.py rna.rmsd rna-noclash > rna-noclash.rmsd
select-lines.py rna.7mer-rmsd rna-noclash > rna-noclash.7mer-rmsd
evaluate rna.rmsd
evaluate rna-noclash.rmsd 

# re-rank by ATTRACT score
select-struct-npy.py rna.npy rna-noclash rna-noclash.npy
npy2pdb.py rna-noclash.npy n3-9r.pdb > rna-noclash.pdb
mkdir rna-noclash-conf
$ATTRACTTOOLS/splitmodel rna-noclash.pdb rna-noclash-conf/conf > rna-noclash.list
python $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/../structure-single.dat $b 2 all > ens.dat
$ATTRACTDIR/attract ens.dat $ATTRACTTOOLS/../attract.par receptorr.pdb \
    rna-noclash-conf/conf-1.pdb --ens 2 rna-noclash.list --score --rcut 50 | \
    awk '$1=="Energy:"{i++; print i, $2}' > rna-noclash.energy
paste rna-noclash.energy  rna-noclash.rmsd |sort -nk2 | awk '{print NR, $4}' > rna-noclash-rescored.rmsd

#cluster
echo "cluster 1 => " > single-clust
seq $b >> single-clust
one-line.sh single-clust
select-struct-npy.py rna.npy rna-noclash rna-noclash.npy

c=0
if [ $b -gt 10000 ];then
    fastcluster_npy.py rna-noclash.npy 10
    s=`awk '{print NF-4}NR==1{exit}' rna-noclash-clust10.0`
    c=10
    if [ $b -gt 10000 ];then
        fastcluster_npy.py rna-noclash.npy 5
        c=5
    fi
fi

for i in 3 2 1; do
    if [ $c -eq 0 ];then
        subcluster-npy.py rna-noclash.npy single-clust $i
    else
        subcluster-npy.py rna-noclash.npy rna-noclash-clust$c.0 $i
    fi
done

for i in 2; do
awk '{print $4}' rna-noclash-clust$i.0 > rna-noclash-clust$i.0-center
select-lines.py rna-noclash.rmsd rna-noclash-clust$i.0-center > rna-noclash-clust$i.0-center-persize.rmsd
#sort -nk1 rna-noclash-clust$i.0-center-persize.rmsd > rna-noclash-clust$i.0-center-perocc.rmsd
select-lines.py rna-noclash.energy rna-noclash-clust$i.0-center > /tmp/bi
paste /tmp/bi rna-noclash-clust$i.0-center-persize.rmsd|sort -nk2 |awk '{print NR, $4}' > rna-noclash-clust$i.0-center-perscore.rmsd
done

if false;then
    for i in 2; do
    awk '{m=$4}NF>4{m=$5}{print m}' rna-noclash-clust$i.0 > rna-noclash-clust$i.0-best
    select-lines.py rna-noclash.rmsd rna-noclash-clust$i.0-best > rna-noclash-clust$i.0-best-persize.rmsd
    #sort -nk1 rna-noclash-clust$i.0-best-persize.rmsd > rna-noclash-clust$i.0-best-perocc.rmsd
    select-lines.py rna-noclash.energy rna-noclash-clust$i.0-best > /tmp/bi
    paste /tmp/bi rna-noclash-clust$i.0-best-persize.rmsd|sort -nk2 |awk '{print NR, $4}' > rna-noclash-clust$i.0-best-perscore.rmsd
    done
fi

for i in 1 2 3; do
evaluate rna-noclash-clust$i.0-center-persize.rmsd
#evaluate rna-noclash-clust$i.0-center-perocc.rmsd
evaluate rna-noclash-clust$i.0-center-perscore.rmsd
evaluate rna-noclash-clust$i.0-best-persize.rmsd
#evaluate rna-noclash-clust$i.0-best-perocc.rmsd
evaluate rna-noclash-clust$i.0-best-perscore.rmsd
done










