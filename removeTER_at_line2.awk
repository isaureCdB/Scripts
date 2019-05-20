BEGIN{i=1}{if ($1=="MODEL") i=0}{ if (i!=0 || $1!="TER") print $0}{if ($1=="ATOM") i=1}
