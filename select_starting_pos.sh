#./select_starting_pos.sh results_per_conformer.list $m-fit-dr0.2r-superclust1.0 start.dat 100

list=$1
clustfile=$2
start=$3
c=$4

./concat_scores.py $list $list-scores.npy $c # > $list-scores-inf$c.npy
bool=$list-scores-inf$c.npy
./ensemblize_custom.py $start $bool $clustfile > $list-scores-inf$c.dat
#/home/isaure/projets/ssRNA/noanchors/4pmw/dock_pocket_lib2018/select_starting_pos.sh
