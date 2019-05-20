awk 'BEGIN{prot=1}{if ($3=="N" && prot==1) {print "TER"; prot=0}}{if ($1=="ATOM" || $1 =="ENDMDL"  || $1 =="MODEL") print $0}{if ($1=="ENDMDL") prot=1}' $1.pdb > ba
mv ba $1.pdb
