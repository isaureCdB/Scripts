#/bin/sh

name=$1
deb=$2
end=$3
x=3
for i in $(seq $2 $3)
do
sed -i "s/\#$i/\#$x/g" $name
((x++))
done
