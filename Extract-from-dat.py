import sys
if len(sys.argv) < 4:
  print >> sys.stderr, "Usage: Extract-from-dat.py <file.dat> <output> <list of ranks to extract>"
  sys.exit()

DAT=open(sys.argv[1],'r')
OUT=open(sys.argv[2],'w')
clusterlist = sorted([int(g) for g in sys.argv[3:]])
#################################################
L=DAT.readlines()
dat=L
deb=0
for l in L:
	line=l.split()
	if len(line)<2:
		deb+=1
		continue
	if line[1]=='SEED':
#		print(line)		
		break
	deb+=1
	OUT.write(l)

l=deb
index=0
seed=0
#print(clusterlist[index])
while l < len(L) and index < len(clusterlist):
	if len(L[l].split())<2:l+=1
	if L[l].split()[1]=='SEED':
#		print('SEED '+str(seed))
		seed+=1
		if seed==clusterlist[index]:
			index+=1
			OUT.write('#%i\n'%index)
			OUT.write('### rank %i befor extracted \n'%seed)
			while len(L[l].split())>1:
				OUT.write(L[l])  
				l+=1
	l+=1

DAT.close()
OUT.close()
