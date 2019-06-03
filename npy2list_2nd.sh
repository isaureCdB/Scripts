for m in `cat motif.list`; do
  if [ ! -s $m/conf-2nd-aa-1.pdb ];then
    echo "create PDB fragments from clust1.0, $m"

    $SCRIPTS/scripts_isaure/npy2pdb.py $m-2nd-aa.npy    templates/$m.pdb > /tmp/$m-clust1.0-aa.pdb
    source activate attract
    python $ATTRACTTOOLS/reduce-npy.py $m-2nd-aa.npy templates/$m.pdb $m-2ndr.npy
    source deactivate
    $SCRIPTS/scripts_isaure/npy2pdb.py $m-2ndr.npy  templates/$m\r.pdb   >  /tmp/$m-clust1.0.pdb

    $ATTRACTTOOLS/splitmodel /tmp/$m-clust1.0.pdb     $m/conf-2ndr > $m-clust1A-2ndr.list
    $ATTRACTTOOLS/splitmodel /tmp/$m-clust1.0-aa.pdb  $m/conf-2nd-aa > $m-clust1A-2nd-aa.list
  fi
done
