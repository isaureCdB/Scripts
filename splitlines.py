#!/usr/bin/env python3

import sys

tosplit=sys.argv[1]
template=sys.argv[2]

i=1
for l in open(tosplit).readlines():
	f=open(template+str(i),"w")
	print(l.strip(), file=f),
	f.close()
	print(template+str(i))
	i+=1
