

echo 10000 > x
for i in 50000 100000 500000 1000000; do echo $i >> x; done

j=$3;for i in `seq $1 $2`; do
    awk -v j=$j '$2<j{i++}(NR==10000||NR==50000||NR==100000||NR==500000||NR==1000000){print 1000*i/NR}' frag$i\r.rmsd > frag$i.enrich-$3\A
    #awk -v j=$j '$2<j{i++}(NR==20000||NR==200000){print 1000*i/NR}' frag$i\r.rmsd > frag$i.enrich-$3\A
done
#paste x frag["$1"-"$2"].enrich-$3\A > enrich-$3\A
paste x frag["$1"-"$2"].enrich-$3\A
