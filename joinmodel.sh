list=$1

j=1
for i in `cat $list`; do
  echo "MODEL $j"
  egrep "ATOM|HETATM|TER" $i
  echo "ENDMDL"
  j=$(($j+1))
done
