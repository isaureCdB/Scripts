#!/usr/bin/python2.7
import sys, os, string

assert len(sys.argv) == 6,  "usage ./anchors.py receptor(.pdb) [anchors.pdb] [frag to anchor for output] [nucleotide to exclude] [beads to print]"

pdb = open(sys.argv[1]+".pdb",'r').readlines()
anchors = open(sys.argv[2],'r').readlines()
frag = str(sys.argv[3])
nucleotide = int(sys.argv[4])
beads = sys.argv[5].split()

os.system("mkdir proteincr_%s"%frag)

AT=int(pdb[-1][7:11])+1
index=1
first=0
at=AT
g=open(sys.argv[1]+"_"+frag+"_Rk"+str(index)+".pdb",'w')

for l in pdb:
  g.write(l)

for line in anchors:
  if line.split()[0]!='ATOM': continue
  if first==0:
    first=int(line[21:30])
    print line
  if int(line[21:30])==first and line[13:16]=='GP1':
    if index!=1:
      g.close()
      g=open(sys.argv[1]+"_"+frag+"_Rk"+str(index)+".pdb",'w')
      print 'print protein'
      at=AT
      for l in pdb:
        g.write(l)
    index+=1
  if int(line[21:30])!=nucleotide and line[13:16] in beads:
    g.write("%s%4d%s%s%s" % (line[:7],at,line[11:57],"99",line[59:]))
    at+=1
g.close()

os.system("mv proteincr_%s_Rk*.pdb proteincr_%s"%(frag,frag))
os.system("ls proteincr_%s/proteincr_%s_Rk*.pdb > proteincr_%s.list"%(frag,frag,frag))
