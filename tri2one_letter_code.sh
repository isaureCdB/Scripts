#/bin/sh
cp $1 BAK$1
sed -i "s/URI/U  /g" $1
sed -i "s/ADE/A  /g" $1
sed -i "s/GUA/G  /g" $1
sed -i "s/CYT/C  /g" $1
sed -i "s/THY/T  /g" $1
sed -i "s/URA/U  /g" $1
