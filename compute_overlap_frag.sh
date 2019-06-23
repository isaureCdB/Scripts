# get the overlap RMSD between all the pairs of poses of two consecutive fragments
# that have overlap RMSD below the given threshold ("cutoff").

cutoff=3 # Maximal overlap cutoff (recommanded : 4 A)

nfrag=`cat boundfrag.list|wc -l`
nposes=10000000

python2 get_msd_build.py

for i in `seq $nfrag`; do

  motif=`awk -v i=$i 'NR==i{print $2}' boundfrag.list`

  if [ ! -s $motif-postatoms.npy ];then
    echo "**********************************************************"
    echo "Extract docking coordinates for $motif"
    echo '**********************************************************'

    # lists of trinucleotide conformers
    # !! you might need to change those names. Look in the nalib directory
    list=nalib/$motif-clust1.0r.list
    template=`head -n 1 $list`

    # convert docking results into binary coordinates
    #
    # preatoms = atoms of the 2 overlapping nucleotides of the upstream fragment
    # postatoms = atoms of the 2 overlapping nucleotides of the downstream fragment
    #
    # you will find the $motif.preatoms and $motif.postatoms on the cluster, at :
    # sbcluster:/data1/isaure/ssRNA/preatoms_postatoms/
    # copy that directory to your computer, softlink in the current directory
    python2 $ATTRACTDIR/dump_coordinates.py $motif-e7.dat $template \
      $motif-preatoms.npy `cat preatoms_postatoms/$motif.preatoms` --ens 2 $list

    python2 $ATTRACTDIR/dump_coordinates.py $motif-e7.dat $template \
      $motif-postatoms.npy `cat preatoms_postatoms/$motif.postatoms` --ens 2 $list

  fi

  ln -s $motif-preatoms.npy frag$i-preatoms.npy
  ln -s $motif-postatoms.npy frag$i-postatoms.npy
done

# Selection of good/bad poses based on the lrmsd toward the bound (reference) structure
awk '$2<=3{print NR}' frag1.lrmsd > frag1-good.list
awk '$2>3{print NR}' frag1.lrmsd > frag1-bad.list

for i in `seq $(($nfrag-1))`; do

  j=$(($i+1))
  awk '$2<=3{print NR}' frag$j.lrmsd > frag$j-good.list
  awk '$2>3{print NR}' frag$j.lrmsd > frag$j-bad.list

  motif1=`awk -v n=$i 'NR==n{print $2}' boundfrag.list`
  motif2=`awk -v n=$j 'NR==n{print $2}' boundfrag.list`

  if [ ! -s frag$i-frag$j\_${cutoff}A.json ];then
    echo ""
    echo "**********************************************************"
    echo "Calculate 2-fragments connections"
    echo "**********************************************************"
    echo ${cutoff}A
    ./connect.py 2 $cutoff $nposes 200 $motif1-preatoms.npy $motif2-preatoms.npy \
      $motif1-postatoms.npy $motif2-postatoms.npy  > frag$i-frag$j\_${cutoff}A.json
  fi

# overlaps > cutoff are note reported
./compute_overlap_frag.py $motif1-preatoms.npy $motif2-postatoms.npy \
  --sel1 frag$i-good.list --sel2 frag$j-good.list \
  --connections frag$i-frag$j\_${cutoff}A.json  > frag$i-frag$j\_good_${cutoff}A.ormsd

./compute_overlap_frag.py $motif1-preatoms.npy $motif2-postatoms.npy \
  --sel1 frag$i-bad.list --sel2 frag$j-bad.list \
    --connections frag$i-frag$j\_${cutoff}A.json   > frag$i-frag$j\bad${cutoff}A.ormsd

done
