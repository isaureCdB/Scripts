import sys

j=0
for l in open(sys.argv[1]).readlines():
    j+=1
    coor = [float(l.split()[j]) for j in range(3)]
    print "ATOM      1  CA  ALA  %4.0f    %8.3f%8.3f%8.3f"%(j, coor[0], coor[1], coor[2])
    
