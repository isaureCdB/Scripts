sed -e 's/ATOM   \(.\{4\}\)  CSE ARG\(.*\) [ 0-9][ 0-9]   0.000 0 1.00/ATOM   \1  CG  ARG\2  3   0.000 0 1.00 \nATOM   \1  NEC ARG\2  4   1.000 0 1.00 /g' $1.pdb > $1-ARG.pdb
