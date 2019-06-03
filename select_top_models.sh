pdb=$1
m=$2
awk -v m=$m 'BEGIN{i=0}$1=="MODEL"{i+=1}i>m{exit}{print $0}' $pdb
