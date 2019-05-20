name=${1%.pdb}
awk 'substr($0,17,1) != "B"' $1 > ${name}A.pdb
awk 'substr($0,17,1) != "A"' $1 > ${name}B.pdb
exit
