#!/bin/bash
#usage dat2pdb .dat protein.pdb ligand(no 'pdb') rank(de 1) output
$ATTRACTTOOLS/top $1 $4 > out
head -n 5 out > out2.dat
tail -n 5 out >> out2.dat
$ATTRACTDIR/collect out2.dat $2 $3\.pdb > out
egrep -v 'SER|TYR|ASP|ASN|ARG|MET|TRP|THR|ALA|CYS|GLU|GLY|PHE|HIS|ILE|LEU|LYS|PRO|VAL|GLN|MODEL|TER|END' out > $5\.pdb
$ATTRACTDIR/reduce_rna $5\.pdb
rm out
rm out2.dat
