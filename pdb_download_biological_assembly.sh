#!/bin/bash
#script to download all assembly units of a pdb entry if they exist,
#else the full pdb

name=$1

j=1
#while true;do
for j in `seq 10`; do
  echo $name $j
  echo " wget 'https://files.rcsb.org/download/'$name'.pdb'$j -O $name-ba$j.pdb"
  if wget 'https://files.rcsb.org/download/'$name'.pdb'$j -O $name-ba$j.pdb ; then
    j=$(($j+1))
  else
    echo "command failed"
    break
  fi
done

if [ $j -eq 1 ]; then
  command="wget 'https://files.rcsb.org/download/'$name'.pdb' -O $name-ba0.pdb"
  echo "------------------------------"
  echo $command
  echo "------------------------------"
  $command
fi
#https://files.rcsb.org/download/1AQ4.pdb2.gz
