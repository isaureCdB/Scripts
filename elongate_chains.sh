#frag1=$1
#frag2=$2
c=2
nstruct=500000
minchild=100
args=" $c $nstruct $minchild "

selfrag(){
  name=${1%*.npz}
  f1=$2
  f2=$3
  chain-propensity-npz.py $name.npz --firstfrag $f1 > /tmp/$name.frags
  for i in `seq $f1 $f2`; do
  	awk -v i=$i '$1==i{print $2}'  /tmp/$name.frags >  /tmp/$name.fragment$i
  	select-lines.py ../frag$i.lrmsd  /tmp/$name.fragment$i --dataorder > /tmp/$name.fragment$i-lrmsd-noorder
  done
  for i in `seq $f1 $f2`; do
    best  /tmp/frag$f1-$f2\_$c\A.fragment$i-lrmsd-noorder
  done
}

elongate_up(){
  f1=$1
  f2=$2
  f=$(($f1-1))
  nfrag=$(($f2-$f1+2))
  selfrag frag$f1-$f2\_$c\A $f1 $f2
  echo "connect-npz.py"
  connect-npz.py $nfrag $args frag$f-$f2\_$c\A.npz frag[$f-$f2]-preatoms.npy frag[$f-$f2]-postatoms.npy /dev/null /tmp/frag$f1-$f2\_$c\A.fragment[$f1-$f2]

}

elongate_down(){
  f1=$1
  f2=$2
  f=$(($f2+1))
  nfrag=$(($f2-$f1+2))
  selfrag frag$f1-$f2\_$c\A $f1 $f2
  connect-npz.py $nfrag $args frag$f1-$f\_$c\A.npz frag[$f1-$f]-preatoms.npy frag[$f1-$f]-postatoms.npy /tmp/frag$f1-$f2\_$c\A.fragment[$f1-$f2]  /dev/null
}

exit
#frag3-6_2A.npz

elongate_down 3 $i

for i in 6 7; do
	echo "elongate_down 2 $i"
	elongate_down 3 $i
done
for i in 3 2; do
	echo "elongate_up 2 $i"
	elongate_up $i 6
done
for j in 6 7; do
    for i in 2 3; do
	    echo "elongate_up 3 $i"
	    elongate_down $i $j
    done
done
