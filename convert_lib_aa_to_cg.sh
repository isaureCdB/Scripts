a=$1
npy2pdb.py $a.npy $a.pdb > /tmp/all.pdb
splitmodel /tmp/all.pdb /tmp/conf > /tmp/all.list
sed 's/conf/confr/' /tmp/all.list > /tmp/r.list
python $ATTRACTTOOLS/reduce.py /tmp/all.list /tmp/r.list --batch
pdb2npy.py /tmp/r.list --outp $a\r.npy --list
