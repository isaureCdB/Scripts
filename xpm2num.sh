#!/bin/bash


#L=(A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x)
#N=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50)
L=(A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n)
N=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40)

Nlines=`wc -l $1.mat|awk '{print $1}'`
l=2676
while [ $l -lt 41000 ];do
	j=$(($l+100))
	sed -n $l","$j"p" $1.mat > bi
	sed -i 's/^"//g' bi
	sed -i 's/\,$//g' bi
	sed -i 's/\"$//g' bi
	for i in `seq 0 50`; do
		sed -i -e "s/${L[$i]}/${N[$i]}\ /g" bi
		done
	cat bi >> $1.num
	l=$(($j+1))
	done

