#!/usr/bin/env python3

import sys, argparse, os, json
'''
usage:
python3 $SCRIPTS/create_alternative_conformer.py $m \
     $m-aa-fit-clust0.2 $m-dr0.2r-clust1.0 \
    --o2nd clust1A-alternate2ndr.list --o3rd clust1A-alternate3rdr.list

  #--o2nd $m-clust1A-2nd --o2ndmap $m-clust1A-2nd.map --o3rd $m-clust1A-3rd  --o3rdmap $m-clust1A-3rd.map
'''

def pp(*x):
    for i in x[:-1]:
        print(i, file=sys.stderr, end=' ')
    print(x[-1], file=sys.stderr)

def mutate(seq, mut):
    mutseq = ""
    for s, m in zip(seq, mut):
        if m:
            c = dict_mutations[s]
        else:
            c = s
        mutseq = mutseq + c
    return mutseq

def find_alternate(clust02_all, js, struct):
    for c02 in clust02_all:
        for i in c02:
            struct2 = js[i]['structure']
            if struct != struct2:
                return i

def find_alternate_all(seq, args, js):
    o2nd = open('%s-%s'%(seq, args.o2nd), 'w')
    #Search for a close fragment that is not from the same PDB
    c02 = "%s-%s"%(seq, args.clust02)
    c1 = "%s-%s"%(seq, args.clust1)
    clust02 = [l.split()[3:] for l in open(c02)]
    clust1 = [[int(j) for j in l.split()[3:]] for l in open(c1)]
    alternate = []
    for nc, c in enumerate(clust1):
        # list of all clust02 in each clust1
        clust02_all = [ clust02[int(x)-1] for x in c ]
        # global indexing of the clust1 center,
        # that is the center of the 1st clust02 in the clust1
        center = clust02_all[0][0]
        #pp((center, seq))
        struct = js[center]['structure']
        # search fisrt in the same clust02 as the clust1 center,
        # then in the rest of the clust1
        a = find_alternate(clust02_all, js, struct)
        print("%i %s"%(nc+1, a), file=o2nd)
    o2nd.close()

def link(seq, mut):
    if mut == (0, 0, 0):
        return
    mutseq = mutate(seq, mut)
    os.system("ln -s %s-%s %s-%s"%(seq, args.o2nd, mutseq, args.o2nd))

#################################################################################
a = argparse.ArgumentParser(prog="fragmt-from-GU.py")
a.add_argument("--frag")        # fragments_ori.json
a.add_argument("--clust02")    # aa-fit-clust0.2 #mapping from all
a.add_argument("--clust1")     # dr0.2r-clust1.0 #mapping from clust0.2
a.add_argument("--o2nd")       # clust1A-2nd
a.add_argument("--na")         #  rna / dna

#a.add_argument("--o3rdmap")   #

args = a.parse_args()
#################################################################################

m = [0,1]
mutations = [(a, b, c) for a in m for b in m for c in m ]
dict_mutations={
  'G':'A',
  'T':'C',
  'U':'C',
  }

s = ['G','U']
if args.na=="dna":
    s = ['G','T']
sequences = [a+b+c for a in s for b in s for c in s ]

frag_json = json.load(open(args.frag))
for seq in sequences:
    # create outputs
    find_alternate_all(seq, args, frag_json[seq])
    for mut in mutations:
        mutate(seq, mut)
        link(seq, mut)
