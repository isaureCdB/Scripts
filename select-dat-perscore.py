import sys
from _read_struc import read_struc
'''
usage: select-dat-perscore.py <dat file> <energy cutoff>
write to the output a dat file containing only the poses with energy above energy cutoff
'''
def check(l1):
    for ll in l1:
        if ll.startswith("## Energy:"):
            ee = ll[10:].strip()
            if ee.startswith("nan") or float(ee) > cutoff :
                return False
    return True

header,structures = read_struc(sys.argv[1])
cutoff = float(sys.argv[2])

structures = list(structures)

for l in header:
    print l

c = 1
for l1,l2 in structures:
    if check(l1):
        print "#%i"%c
        for l in l1 + l2:
            print l
        c+=1
    else:
        break
