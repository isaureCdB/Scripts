#/bin/sh

name=$1

Xray_protein_bound=Xray_protein_bound.pdb; Xray_NA_bound=Xray_NA_bound.pdb; Xray_protein=Xray_protein.pdb; Xray_NA=Xray_NA.pdb

if [ -f Xray_NA-cut.pdb ]; then Xray_NA=Xray_NA-cut.pdb;fi
if [ -f Xray_NA_bound-cut.pdb ]; then Xray_NA_bound=Xray_NA_bound-cut.pdb;fi
if [ -f Xray_protein-cut.pdb ]; then Xray_protein=Xray_protein-cut.pdb;fi
if [ -f Xray_protein_bound-cut.pdb ]; then Xray_protein_bound=Xray_protein_bound-cut.pdb;fi
echo "python $ATTRACTDIR/irmsd.py ${name} $Xray_protein $Xray_protein_bound $Xray_NA $Xray_NA_bound --allatoms > ${name}.irmsd"
python $ATTRACTDIR/irmsd.py ${name} $Xray_protein $Xray_protein_bound $Xray_NA $Xray_NA_bound --allatoms > ${name}.irmsd
awk '{print NR,$2}' ${name}.irmsd|sort -nk2 > ${name}.irmsd-sorted
