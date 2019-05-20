nalib=/data1/isaure/nalib_05_2018/

for m in `cat motif.list`; do
    unlink $m-clust1Ar.list
    unlink $m-clust1A-aa.list
    ln -s $nalib/$motif
    cp $nalib/$m-clust1A.list .
    cp $nalib/$m-clust1A-aa.list .
    for i in `awk -v m=$m '$2==m{print $1}' boundfrag.list` ; do
        bb=`awk '$2<0.01{print $1}' frag${i}r.rmsd|wc -l`
        if [ $bb == "1" ]; then
            #b = rank of the bound form
            b=`awk '$2<0.01{print $1}' frag${i}r.rmsd`
            #
            awk -v b=$b 'NR<b' $m-clust1Ar.list > $m-clust1Ar.list-nobound
            awk -v b=$b '$1==b{print $2}' $m-clust1A-alternate2ndr.list >> $m-clust1Ar.list-nobound
            awk -v b=$b 'NR>b' $m-clust1Ar.list >> $m-clust1Ar.list-nobound
            mv $m-clust1Ar.list-nobound  $m-clust1Ar.list
            #
            awk -v b=$b 'NR<b' $m-clust1A-aa.list > $m-clust1A-aa.list-nobound
            awk -v b=$b '$1==b{print $2}' $m-clust1A-alternate2nd-aa.list >> $m-clust1A-aa.list-nobound
            awk -v b=$b 'NR>b' $m-clust1A-aa.list >> $m-clust1A-aa.list-nobound
            mv $m-clust1A-aa.list-nobound  $m-clust1A-aa.list
            #
        fi
    done
done
