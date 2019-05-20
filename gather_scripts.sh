p=`pwd`
for i in `ls *.py */*.py */*/*/*.py */*.sh */*/*.sh`; do
    a=`echo $i|awk -F '/' '{print $NF}'`
    if [ ! -s $SCRIPTS/$a ];then
        echo $i
        cp -L $i  /home/isaure/Scripts/$a
        echo "#$p/$a" >> /home/isaure/Scripts/$a
    fi
done
