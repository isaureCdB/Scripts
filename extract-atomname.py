import sys, os
import numpy
sys.path.insert(0, os.environ["ATTRACTTOOLS"])
import rmsdlib

pdblist = sys.argv[1]
atomnames = [j.rstrip() for j in  open(sys.argv[2],'r').readlines()]
print sys.argv, atomnames
towrite=[]

atomnamestr="-".join(atomnames).replace("'","p")
outf = open('contain-'+atomnamestr+'.pdb', "w")

for i in open(pdblist,'r').readlines():
  i=i.strip()
  for p in rmsdlib.read_multi_pdb(i):    
    for pdb in p:
      for res in pdb.residues():
       PO3=False
       for a in res:
         if a.name in atomnames: PO3=True
       if PO3:
          print >> outf, 'MODEL'        
          for a in res:
             a.write(outf)
          print >> outf, 'ENDMDL'        
          
#towrite.rmsdlib.write('contain-'+atomnamestr+'.pdb')

