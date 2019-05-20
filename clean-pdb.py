import sys

for l in open(sys.argv[1]).xreadlines():
    if l[:6] == 'ANISOU':
        continue
    if l[:6] == 'HETATM' and l[17:20] in ("MET", "MSE"):
        if l[12:15].split() == "SE":
            print "ATOM  "+l[6:12]+" SD"+l[15:17]+"MET"+l[20:-1]
        else:
            print "ATOM  "+l[6:17]+"MET"+l[20:-1]
    else:
        print l,

