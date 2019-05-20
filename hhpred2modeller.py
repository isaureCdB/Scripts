#!/usr/bin/env python3
import sys, argparse

#######################
parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('hhr') #hhpred_x.hhr
parser.add_argument('template') #pdbcode
parser.add_argument('fasta')  #query.fasta
parser.add_argument('--oligo', type=int)  #query.fasta

args = parser.parse_args()
#######################
hhr = args.hhr #hhpred_x.hhr
template = args.template #pdbcode
fasta = args.fasta #query.fasta

oligo = 1
if args.oligo is not None:
    oligo  = args.oligo

if len(sys.argv) < 4:
    print('usage: hhpre2modeller.py hhpred_x.hhr pdbcode query.fasta')

res1, chain1 = 0, ''
for l in open('%s.pdb'%template, 'r').readlines():
    if l.startswith('ATOM'):
        if res1==0:
            res1 = int(l[22:26])
            chain1 = l[21]
        res2 = int(l[22:26])
        chain2 = l[21]

Nres = 0
for l in open(fasta).readlines()[1:]:
    Nres += len(l.strip())

print('>P1;query')
print('sequence:query:1:A:%i:A::::'%Nres)

hit = 0
sequence = ''
structure = ''
for l in open(hhr,'r').readlines():
    if l[1:5] == template:
        hit=1
    if not hit: continue
    ll = l.split()
    if l[:4] == "Q Q_":
        sequence = sequence + ll[3]
    if l[0] == 'T' and l[2:6] == template:
        structure = structure + ll[3]
    if l[:2] == 'No':
        print(sequence, end='')
        for i in range(1,oligo):
            print('/')
            print(sequence, end='')
        print('*')
        print('')
        print('>P1;%s'%template)
        print('structure:%s:%i:%s:%i:%s::::'%(template, res1, chain1, res2, chain2))
        print(structure, end='')
        for i in range(1,oligo):
            print('/')
            print(structure, end='')
        print('*')
        break
