nalib=/data1/isaure/nalib_05_2018/
for m in `cat motif.list`; do
    #unlink $m-clust1Ar.list
    #unlink $m-clust1A-aa.list
    #cp $nalib/$m-clust1Ar.list .
    #cp $nalib/$m-clust1A-aa.list .
    for i in `awk -v m=$m '$2==m{print $1}' boundfrag.list` ; do
        bb=`awk '$2<0.01{print $1}' frag${i}r.rmsd|wc -l`
        if [ $bb == "1" ]; then
            b=`awk '$2<0.01{print $1}' frag${i}r.rmsd`
            #
            awk -v b=$b 'NR<b' $nalib/$m-clust1Ar.list > $m-clust1Ar.list2
            awk -v b=$b 'NR==b' $nalib/$m-clust1A-alternate2ndr.list >> $m-clust1Ar.list2
            awk -v b=$b 'NR>b' $nalib/$m-clust1Ar.list >> $m-clust1Ar.list2
            mv $m-clust1Ar.list2 $m-clust1Ar.list-nobound
            #
            awk -v b=$b 'NR<b' $nalib/$m-clust1A-aa.list > $m-clust1A-aa.list2
            awk -v b=$b 'NR==b' $nalib/$m-clust1A-alternate2nd-aa.list >> $m-clust1A-aa.list2
            awk -v b=$b 'NR>b' $nalib/$m-clust1A-aa.list >> $m-clust1A-aa.list2
            mv $m-clust1A-aa.list2 $m-clust1A-aa.list-nobound
            #
        fi
    done
done
