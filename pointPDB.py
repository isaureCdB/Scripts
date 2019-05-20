#!/usr/bin/python2.7
import sys

coord = [ float(i) for i in sys.argv[1:4] ]
l="ATOM      1  C5'  G5     3     -17.305  -3.945  13.542  1.00  0.00"
print l[:30]+"%8.3f%8.3f%8.3f"%(coord[0], coord[1], coord[2])+l[54:],

