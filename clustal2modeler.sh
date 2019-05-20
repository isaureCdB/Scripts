
alignment=$1    # txt file containing the alignment from Clustal-Omega
template=`awk 'NR==1{print $1}' $alignment`
model=`awk 'NR==2{print $1}' $alignment`  

$SCRIPTS/prep-template.sh $template.pdb
sed -i 's/-/X/g' $alignment

nres=`egrep 'ATOM|HETATM' $template.pdb |tail -n 1|awk '{print substr($0,23,4)}'`
chain=`awk '$1=="ATOM"{print substr($0,22,1); exit}' $template.pdb`

echo ">P1;$template" > $template.ali
echo "structure:$template:1:$chain:$nres:$chain::::" >> $template.ali
awk -v i=$template '$1==i{print $2}END{print "*"}' $alignment >> $template.ali

echo "" >> $template.ali
echo ">P1;$model" >> $template.ali
echo "sequence:$model:1:A:999:A::::" >> $template.ali

awk -v i=$model '$1==i{print $2}END{print "*"}' $alignment >> $template.ali

sed -i 's/X/-/g' $template.ali

