ls *excise.pdb|awk -F "-iniparse" '{print $1}' > models.list

for i in `cat models.list`; do 
	echo "----------------------------- $i"
	a=`md5sum $i-iniparse.pdb |awk '{print $1}'`
	b=`md5sum $i-iniparse-excise.pdb |awk '{print $1}'`
	c=`md5sum $i-iniparse-excise-aa.pdb |awk '{print $1}'`
	echo $a $b $c
	if [ -s $i-iniparse-excise.pdb ] && [ -s $i-iniparse.pdb  ]; then
		if [ $a == $b ];then 
			rm $i-iniparse-excise.pdb
			ln -s $i-iniparse.pdb $i-iniparse-excise.pdb
		fi
	fi
	if [ -s $i-iniparse-excise-aa.pdb ] && [ -s $i-iniparse.pdb  ]; then
		if [ $a == $c ]; then
			rm $i-iniparse-excise-aa.pdb
			ln -s $i-iniparse.pdb $i-iniparse-excise-aa.pdb
		fi
	fi
done
