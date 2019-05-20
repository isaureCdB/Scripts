n=${1%%.pdb}
awk '($1=="MODEL" && $2==2){exit}{print $0}' $n.pdb > $n-1.pdb
