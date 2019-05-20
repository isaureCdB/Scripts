complex=$1 #complex.pdb
na=$2
nalib=$3

if false;then
  center $complex > complexc.pdb
  python $ATTRACTDIR/../allatom/aareduce.py complexc.pdb --$na --heavy --nalib --manual --termini
  NA=RNA
  if [ $na == "dna" ]; then NA=DNA ; fi
  egrep " [DR][AUCGT] " complexc-aa.pdb|egrep -v "XXX|O5T" > ${NA}-aa.pdb
  egrep -v ' [DR][AUCG] ' complexc-aa.pdb|uniq > protein-aa.pdb

  for i in protein ${NA}; do
      renum-at-res.py $i-aa.pdb > /tmp/bi; mv /tmp/bi $i-aa.pdb
  done
fi

python $ATTRACTTOOLS/reduce.py protein-aa.pdb > /dev/null
python $ATTRACTTOOLS/reduce.py ${NA}-aa.pdb --${na} > /dev/null
#fi
ln -s protein-aar.pdb receptorr.pdb

Nnucl=`egrep 'GP1' ${NA}-aar.pdb|wc -l`
mkdir boundfrag
for i in `seq $(($Nnucl-2))`;do
    j=$(($i+1))
    k=$(($i+2))
    egrep ' [ DR][ATUCG] [A-Z| ] *('$i'|'$j'|'$k') ' ${NA}-aar.pdb > boundfrag/frag$i\r.pdb
    egrep ' [ DR][ATUCG] [A-Z| ] *('$i'|'$j'|'$k') ' ${NA}-aa.pdb >  boundfrag/frag$i-aa.pdb
done
#fi

cat /dev/null > boundfrag.list
n=`ls -l boundfrag/frag*r.pdb|wc -l`
for i in `seq $n`; do
    awk -v i=$i 'BEGIN{j=1}j==3&&$3=="GP1"{c=substr($4,2,1)}\
                j==2&&$3=="GP1"{b=substr($4,2,1);j=3}\
                j==1&&$3=="GP1"{a=substr($4,2,1);j=2}\
                END{printf("%i %s%s%s\n",i,a,b,c)}'\
                boundfrag/frag$i\r.pdb >> boundfrag.list
done
awk '{print $2}' boundfrag.list|sort -u > motif.list
$SCRIPTS/eval_bound_form.sh $nalib
$SCRIPTS/remove_bound_frag_rmsd_cutoff.sh $nalib
