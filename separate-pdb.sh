#/bin/sh

#echo $Nstruct 32597120

#sed -n -e '/MODEL \+1$/,/END/p' $1 > x
awk '{print $0}{if ($1=="ENDMDL") {exit}}' $1 > x
nlines=`wc -l x|awk '{print $1}'`

split -d -l $nlines $1 $2

