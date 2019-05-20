import sys

vect = [float(sys.argv[i]) for i in range(1,4)]

for l in open(sys.argv[1]).xreadlines():
    if not startswith("ATOM"):
        print l
    else
        coor = [float(i) for i in l[29:38], l[38:46], l[46:54])
        newcoor = [ str(coor[i]+vect[i]) for i in range(3)]
        printf +l[29:38]+"MET"+l[20:-1]
        print l[:30]+"%8.3f%8.3f%8.3f"%(COM[0], COM[1], COM[2])+l[54:]
