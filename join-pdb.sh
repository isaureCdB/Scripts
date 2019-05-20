list=$1
j=1
for i in `cat $list`; do
  echo "MODEL $j"
  awk '$1=="ATOM"||$1=="HETATM"||$1=="TER"' $i
  j+=1
  echo "ENDMDL"
done
