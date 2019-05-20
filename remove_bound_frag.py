#!/usr/bin/env python3

struct = sys.argv[1]        # 1B7F
list = sys.argv[2]          # nalib/${motif}r.list
list2nd = sys.argv[3]       # nalib/${motif}r-2nd.list
o2nd = sys.argv[4]          #nalib/${motif}-clust1A-2nd

#################### ${motif}r-2nd.list
# UUU/confr-2nd-1.pdb
# UUU/confr-2nd-2.pdb

#################### ${motif}-clust1A-2nd
# 1 123654 struct
# 2 545 struct
# 3 None struct
# 4 3593  struct
# 5 40 struct

conf = [ l.split()[0] forl in open(list)]
conf2nd = [ l.split()[0] forl in open(list2nd)]

nconf = 0
for nl, l in open(o2nd):
    ll = l.split()
    if ll[2] == struct:
        if ll[1] != None:
            print(conf2nd[nconf])
    else:
        print(conf[nconf])
    if ll[1] != None:
        nconf+=1
