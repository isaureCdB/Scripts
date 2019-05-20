pdb=$1
m=$2
awk -v m=$m '$1=="MODEL"&&$2==m{i==1}i=1{print $0}$1=="ENDMDL"&&i==1{exit}' $pdb
