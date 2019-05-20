$ATTRACTTOOLS/top $1.dat $2 > $1-$2.dat
egrep -v '0.000000( | -)0.000000( | -)0.000000( | -)0.0000( | -)0.0000( | -)0.0000' $1-$2.dat|tail -n +2 > $1-$2-lig.dat
sed -i 's/pivot 2/pivot 1/g' $1-$2-lig.dat

collect $1-$2-lig.dat  $3  --single > $1-$2-lig.pdb
