m=$1 #n_nucl
npy=$2

awk -v m=$m '$5<=m' boundfrag/RNAr.pdb > /tmp/$m\mer.pdb
awk '$5<=3' boundfrag/RNAr.pdb > /tmp/3mer.pdb


select-struct-npy.py rna.npy 1 /tmp/1.npy
npy2pdb.py /tmp/1.npy /tmp/$m\mer.pdb > /tmp/1.pdb
head -n 2 /tmp/1.pdb|tail -n 1

n=`head -n 1 chains.txt|awk '{print $1}'`
select-struct-npy.py $npy $n /tmp/pose1.npy
npy2pdb.py /tmp/pose1.npy /tmp/3mer.pdb > /tmp/pose1.pdb
head -n 2 /tmp/pose1.pdb|tail -n 1
