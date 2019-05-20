grep 0000 $1.xvg |awk '{print 10*$2}' > $1.lrmsd
