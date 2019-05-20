BEGIN{i=0}($1=="MODEL" && $2==1){i=1}(i==1){print $0}($1=="MODEL" && $2=="2"){exit}
