sed 1,66d $1.xpm > $1.txt
sed -i 's/^"//g' $1.txt
sed -i 's/\,$//g' $1.txt
sed -i 's/\"$//g' $1.txt
#for lettre in A B C D E F G H I J;do sed -i -e "s/$lettre/$lettre /g" $1.txt;done
sed -i 's/\(.\)/\1 /g' $1.txt
