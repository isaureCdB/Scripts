a=`ps -elf|grep "sshfs ichauvot@newton:/home/isaure /home/"|awk '$15=="sshfs"{print $4}'`
for i in $a; do
    kill -9 $i
done
fusermount -u /home/isaurec/newton
sshfs ichauvot@newton:/home/isaure ~/newton/
