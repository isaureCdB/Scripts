import sys

multipdb = open(sys.argv[1])
separator = sys.argv[2]
name = sys.argv[3]

i = 0
for l in multipdb:
    if l.startswith(separator):
        i += 1
        outp = open("%s-%d.pdb"%(name, i), "w")
        continue
    print >> outp, l

