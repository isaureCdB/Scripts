#!/bin/bash

name=${1%%.pdb}

#awk 'substr($0,57, 2)!="99"{print substr($0, 1, 54), " 1.00 47.11           N"}' $name-heavy.pdb > /tmp/bi
#renum-at-res.py /tmp/bi > $name-heavy-radii.pdb

/home/isaure/software/eros2.0.5.x64 -testprobe -probe=1.4 $name.pdb
