#generate single-model conformers from a multi-pdb file "results.pdb"
#list them in "results.list"
mkdir results
python $ATTRACTTOOLS/splitmodel.py results.pdb results/conf > results.list

#create "fake" docking results with all trnasformation set to None
nconf=`cat results.list|wc -l`
python $ATTRACTTOOLS/ensemblize.py $ATTRACTTOOLS/..//structure-single.dat $nconf 2 all > ens.dat

#compute l-RMSD i-RMSD and fnat
python $ATTRACTDIR/lrmsd.py ens.dat `head -n 1 results.list` bound_lig.pdb --allatoms --ens 2 results.list > results.lrmsd
python $ATTRACTDIR/irmsd.py ens.dat unbound_rec.pdb bound_rec.pdb `head -n 1 results.list` bound_lig.pdb --allatoms --ens 2 results.list > results.irmsd
python $ATTRACTDIR/irmsd.py ens.dat $cutoff unbound_rec.pdb bound_rec.pdb `head -n 1 results.list` bound_lig.pdb --allatoms --ens 2 results.list > results.fnat

