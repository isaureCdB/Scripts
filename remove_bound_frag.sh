#for m in `cat motif.list`; do
#    ln -s /home/isaure/projets/ssRNA/nalib/$m
#done

chain=$1
remove_bound_frag.py $chain motif.list /home/isaure/projets/ssRNA/nalib-09-2017/chaindata/pdbfiles-GU.list
