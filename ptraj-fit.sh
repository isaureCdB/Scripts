# Se placer dans "analyses"

Nstruct=$1
rena2=$2 	#1st res of protein

echo "/home/daniel/amber12/bin/ptraj conf1.pdb <<!" > ptraj-lrmsd
for i in $(seq 1 $Nstruct); do
echo "trajin $i.pdb" >> ptraj-lrmsd
done
echo "reference conf1.pdb" >> ptraj-lrmsd
echo "rms reference" >> ptraj-lrmsd
echo "trajout ../bsf_fit.binpos binpos append" >> ptraj-lrmsd
echo "!" >> ptraj-lrmsd
chmod +x ptraj-lrmsd
./ptraj-lrmsd > ptraj-lrmsd.log
