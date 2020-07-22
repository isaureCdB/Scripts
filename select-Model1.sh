awk '($1=="MODEL" && $2==2){exit}{print $0}' $1.pdb > $1-1.pdb
