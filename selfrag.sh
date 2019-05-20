best(){
echo "---------------- $1"
awk '$2<6.05' $1|sort -nk2|head -n 5
}

nn=${1%*.npz}
name=${nn#*/}
f1=$2
f2=$3

chain-propensity-npz.py $name.npz --firstfrag $f1 > /tmp/$name.frags
for i in `seq $f1 $f2`; do
	awk -v i=$i '$1==i{print $2}'  /tmp/$name.frags >  /tmp/$name.fragment$i
	select-lines.py frag$i.lrmsd  /tmp/$name.fragment$i --dataorder > /tmp/$name.fragment$i-lrmsd-noorder
done
for i in `seq $f1 $f2`; do
	best  /tmp/$name.fragment$i-lrmsd-noorder
done
