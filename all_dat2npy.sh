for f in `ls *.dat`; do
	a=${f%".dat"}
	echo $a
	if [ ! -s $a.dat.npy ];then
		if [ -s $a.score ];then
			dat2npy.py $a.dat --score $a.score
		else :
			dat2npy.py $a.dat
		fi
	fi
	if [ -s $a.dat.npy ]; then
		rm $a.dat
		if [ -s $a.dat.npy ]; then
			rm $a.score
		fi
	fi
	
done
