#!/bin/bash

name=$1 # top50000
list=$2 # list of complexes
#run=$3 # testingSampling29102017
d=`pwd`
run=$3
x=$RANDOM
###################################
d=`pwd`
for i in `cat $list`; do
    echo $i
    cd $i/$run/
    pwd
    if [ ! -s $name-count_stars.txt ];then #########################################
      # !!! rmsd and fnat and irmsd must be computed with the NON-REDUCED complexes !!!
      # e.g.  1ACBA.pdb, not r1ACBA.pdb
      paste $name.lrmsd  $name.irmsd $name.fnat > /tmp/$x-$name-irmsd-fnat
      awk '{i=0} ($2<10.05 || $4<4.05) && $5>=0.1{i=1}\
                 ($2<5.05 || $4<2.05) && $5>=0.3{i=2}\
                 ($2<1.05 || $4<1.05) && $5>=0.5{i=3}\
                 {print i}' /tmp/$x-$name-irmsd-fnat > $name-stars.txt
      cat /dev/null > $name-count_stars.txt
      for n in 1 10 100 1000 50000; do
        awk -v n=$n 'BEGIN{i=0;j=0;k=0}\
                    $1>=1{i++}$1>=2{j++}$1==3{k++}\
                    NR==n{print "top "n": ", i, j, k; exit}' $name-stars.txt >> $name-count_stars.txt
      done
    fi ######################################################################
    cd $d
done

cat /dev/null > $run\_$name-stars.txt

for n in 1 10 100 1000; do
    cat /dev/null > /tmp/$x-stars
    for j in `cat $list`; do
        grep "top $n: " $j/$run/$name-count_stars.txt >> /tmp/$x-stars
    done
    awk -v n=$n 'BEGIN{i=0;j=0;k=0}$3>0{i++}$4>0{j++}$5>0{k++}NR==n{print "top"n": ",  i, j, k}' /tmp/$x-stars >> $run\_$name-stars.txt
done
#fi
