egrep -v "(\ |')H(A|B|D|E|O|G|H|Z|[1-9]|\ )[0-9 'T]" $1.pdb > bou
mv bou $1-noH.pdb
