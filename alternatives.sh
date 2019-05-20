c2=confr-fit-clust0.2
c1=confr-fit-clust0.2-clust1.0
d=`pwd`

align2(){
  echo 1 > sel1
  select-struct-npy.py conf-aa.npy sel1 conf-aa-1.npy
  npy2pdb.py conf-aa-1.npy template-aa.pdb > conf-aa-1.pdb
  fit_multi_npy.py $c1\_alternative-aa.npy bi.npy --npyref conf-aa-1.npy
  mv bi.npy $c1\_alternative-aa.npy
}
for i in UUU UUG UGU GUU UGG GUG GGU GGG; do
#for i in GUU ;do
    cd $d/$i
    echo $i
    python3 $SCRIPTS/replace_bound.py $c2 $c1 UUU chainname.txt confr-fit-clust1.0.sel
    awk '$1=="none"{exit}{print $1}' $c1.alternative > alternative.list
    awk '$1!="none"{print NR}' $c1.alternative > $c1.alternative-mapping
    awk '$1!="none"' $c1.alternative > $c1.alternative-nonone
    select-struct-npy.py conf-aa.npy $c1.alternative-nonone $c1\_alternative-aa.npy
    align2 ### fit $c1.alternative-aa.npy
    npy2pdb.py $c1\_alternative-aa.npy template-aa.pdb > $c1\_alternative-aa.pdb
    python $ATTRACTTOOLS/splitmodel.py $c1\_alternative-aa.pdb conf-alternative/pre-conf-aa > /dev/null
    rm $c1\_alternative-aa.pdb
    cat /dev/null > conf-alternative-aa.list
    cat /dev/null > conf-alternativer.list
    j=1
    for i in `cat $c1.alternative-mapping`; do
        #echo $j $i
        mv conf-alternative/pre-conf-aa-$j.pdb conf-alternative/conf-aa-$i.pdb
        python $ATTRACTTOOLS/reduce.py conf-alternative/conf-aa-$i.pdb conf-alternative/confr-$i.pdb --rna > /dev/null
        echo "conf-alternative/conf-aa-$i.pdb" >> conf-alternative-aa.list
        echo "conf-alternative/confr-$i.pdb" >> conf-alternativer.list
        j=$(($j+1))
    done
done

#exit
cd $d
for i in UUU UUG UGU GUU UGG GUG GGU GGG; do
    for a in "-aa" "r"; do
        unlink $i-clust1A$a-2nd.list
        ln -s $i/conf-alternative$a.list $i-clust1A$a-2nd.list
    done
done

exit
#######################################################
align1(){
    echo 1 > sel1
    select-struct-npy.py confr-fit.npy sel1 confr-fit-1.npy
    select-struct-npy.py conf-aa.npy sel1 conf-aa-1.npy
    npy2pdb.py confr-fit-1.npy templater.pdb > confr-fit-1.pdb
    npy2pdb.py conf-aa-1.npy template-aa.pdb > conf-aa-1.pdb
    python $ATTRACTTOOLS/reduce.py conf-aa-1.pdb --rna > /dev/null
    python $ATTRACTTOOLS/fit.py confr-fit-1.pdb conf-aa-1r.pdb --allatoms > conf-aa-1r-fit.pdb
    e=`python $ATTRACTTOOLS/euler.py conf-aa-1r.pdb conf-aa-1r-fit.pdb`
    p=`COM.py conf-aa-1r.pdb`
    echo "#pivot 1 0 0 0" > sel1.dat
    echo "#pivot 2 $p" >> sel1.dat
    echo "#centered receptor: false" >> sel1.dat
    echo "#centered ligand: false" >> sel1.dat
    echo "#1" >> sel1.dat
    echo " 0 0 0 0 0 0" >> sel1.dat
    echo " $e" >> sel1.dat
    collect sel1.dat  /dev/null conf-aa-1.pdb > conf-aa-1-fit.pdb
    fit_multi_npy.py --pdb conf-aa-1-fit.pdb $c1\_alternative-aa.npy bi.npy
    mv bi.npy $c1\_alternative-aa.npy
    rm confr-fit-1.npy conf-aa-1.npy confr-fit-1.pdb conf-aa-1.pdb conf-aa-1r.pdb conf-aa-1r-fit.pdb
}
