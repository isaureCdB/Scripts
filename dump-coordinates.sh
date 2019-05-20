#cd $PBS_O_WORKDIR

f=$1
r=$2 # "" (coarse-grain) or "-aa" (all-atom)
list=$3
pdb=`head -n 1 $list`

set -u -e
python $ATTRACTDIR/dump_coordinates.py ens.dat $pdb frag$f-preatoms$r.npy `cat frag$f.preatoms$r` --ens 2 $list
python $ATTRACTDIR/dump_coordinates.py ens.dat $pdb frag$f-postatoms$r.npy `cat frag$f.postatoms$r` --ens 2 $list
