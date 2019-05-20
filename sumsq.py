import sys, math

#l = [int(l.split()[0]) for l in open(sys.argv[1]).readlines()]
l=[int(i) for i in sys.argv[1:] ]
k=0
for i in l:
    k+=math.log10(i)

print k
