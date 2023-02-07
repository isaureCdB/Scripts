ls *.pdb > models.list

d=$1 #directory with link targets

for i in `cat models.list`; do 
	if [ -s $i ] && [ -s $d/$i ]; then
		a=`md5sum $i |awk '{print $1}'`
		b=`md5sum $d/$i |awk '{print $1}'`
		if [ $a == $b ];then 
			rm $i
			ln -s $d/$i $i
		fi
	fi
done
