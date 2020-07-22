#!/bin/bash
name=${1%".dat"}
echo "ATOM     21  GG4  RG     3      -0.000  -0.000  -0.000" > zero.pdb
$ATTRACTDIR/collect $name.dat /dev/null zero.pdb > /tmp/bi
grep ATOM  /tmp/bi | uniq > $name.pdb
