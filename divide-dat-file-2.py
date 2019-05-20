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
H=run("head -n 30 "+sys.argv[1]+".dat > deb.dat")
Nseeds=int(sys.argv[2])

run("egrep 'pivot|centered' deb.dat > head.dat")

n=int(subprocess.check_output("sed -n -e '/\#1$/,/\#2$/p' deb.dat | wc -l |awk '{print $1}' ", shell=True))-1
print('n='+str(n))

head = int(subprocess.check_output("wc -l head.dat|awk '{print $1}'", shell=True))
Nlines = int(subprocess.check_output("wc -l "+sys.argv[1]+".dat|awk '{print $1}' ", shell=True))

r=1
deb=head+1
fin=deb+Nseeds*n-1
run('cat head.dat > '+sys.argv[1]+'-'+str(r)+'.dat')
run('sed -n "'+str(deb)+','+str(fin)+'p" '+sys.argv[1]+'.dat >> '+sys.argv[1]+'-'+str(r)+'.dat')
deb+=Nseeds*n
r+=1
while deb in range((Nlines-n)+1):
	fin=deb+Nseeds*n-1
	run('cat head.dat > '+sys.argv[1]+'-'+str(r)+'.dat')
	run('sed -n "'+str(deb)+','+str(fin)+'p" '+sys.argv[1]+'.dat >> '+sys.argv[1]+'-'+str(r)+'.dat')
	run('/home/ichauvot/Scripts/renum-dat.py '+sys.argv[1]+'-'+str(r))
	run('mv '+sys.argv[1]+'-'+str(r)+'-renum.dat '+sys.argv[1]+'-'+str(r)+'.dat')
	deb+=Nseeds*n
	r+=1

