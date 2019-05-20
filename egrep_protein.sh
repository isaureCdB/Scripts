awk '$1=="ATOM"||$1=="MODEL"||$1=="ENDMDL"||$1=="TER"' $1 > /tmp/ba

egrep "GLU|CYS|LYS|THY|MET|LEU|HIS|ARG|SER|TRP|ASN|HIE|PRO|CYX|GLN|PHE|GLY|ALA|ILE|ASP|THR|TYR|HIP|MSE|VAL|TER|MODEL|ENDMDL" /tmp/ba > /tmp/bi

sed -i 's/SE   MSE/ SD  MSE/' /tmp/bi

sed -i 's/ MSE / MET /' /tmp/bi

sed  's/ CYX / CYS /' /tmp/bi

exit

for i in `awk '{print $1}' get_benchmark_from_RNAfrag.log`; do
  for c in `awk -v i=$i '$1==i{print $2}' get_benchmark_from_RNAfrag.log`; do
    cp $i-prot.pdb $i-$c/receptor.pdb
    cp $i-protr.pdb $i-$c/receptorr.pdb
  done
done
