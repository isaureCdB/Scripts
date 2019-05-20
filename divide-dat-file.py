#!/usr/bin/python2.7
###########################
###  L I P R A R I E S  ###
###########################
import sys
import os
import subprocess
#################################################
def run(command):
  sys.stdout.flush()
  os.system(command)
#################################################
P=subprocess.check_output("head -n 20 "+sys.argv[1]+".dat ", shell=True).split('\n')
Nseeds=int(sys.argv[2])

seed=0
i=0
j=0
print(len(P))
while i in range(len(P)):
	if len(P[i].split())==1:
		if seed==0:
			head=i
			print('head='+str(head))
		seed+=1
		if seed==1:
			j=i-head-1
			print('j='+str(j))
			break
	i+=1

Nlines = int(subprocess.check_output("wc -l "+sys.argv[1]+".dat|awk '{print $1}' ", shell=True))

r=1
deb=head+1
while deb in range((Nlines-j)+1):
	fin=deb+Nseeds*j
	run('head -n '+str(head)+' '+sys.argv[1]+'.dat > '+sys.argv[1]+'-'+str(r)+'.dat')
	run('sed -n "'+str(deb)+','+str(fin)+'p" '+sys.argv[1]+'.dat >> '+sys.argv[1]+'-'+str(r)+'.dat')
	run('/home/ichauvot/Scripts/renum-dat.py '+sys.argv[1]+'-'+str(r))
	run('mv '+sys.argv[1]+'-'+str(r)+'-renum.dat '+sys.argv[1]+'-'+str(r)+'.dat')
	deb+=Nseeds*j+1
	r+=1
	

