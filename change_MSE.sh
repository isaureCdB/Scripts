awk '$1=="ATOM"||$1=="HETATM"||$1=="TER"' $1 |egrep "GLU|CYS|LYS|THY|MET|LEU|HIS|ARG|SER|TRP|ASN|HIE|PRO|CYX|GLN|PHE|GLY|ALA|ILE|ASP|THR|TYR|HIP|MSE|VAL|TER" > /tmp/bi
sed -i 's/SE   MSE/ SD  MSE/' /tmp/bi
sed -i 's/ MSE / MET /' /tmp/bi
sed  's/HETATM/ATOM  /' /tmp/bi > $1
