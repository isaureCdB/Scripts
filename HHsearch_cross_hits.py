import sys

hhr = []
for a in sys.argv[1:]:
    hhr.append([])
    b=open(a).readlines()
    for l in b:
        ll = l.split()        
        for i in range(len(ll)):        
            if ll[i] == "PDB:":
                 for j in range(i+1,len(ll)):
                    hhr[-1].append(ll[j][:4])
        if l[0]==">":
            hhr[-1].append(l[1:5])

cross = []
for pdb in set(hhr[0]):
    hit = 1
    for h in hhr[1:]:
        if pdb not in set(h):
            hit = 0
    if hit:
        print pdb   

