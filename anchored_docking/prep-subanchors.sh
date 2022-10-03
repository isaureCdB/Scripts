set -u -e

wd=`pwd`;dir=`dirname $0`;cd $dir;scripts=`pwd`;cd $wd

frag=$1  ## integer. already docked
Nsubanchors=$2 # Nb of subanchors to use for this docking. integer or "all"
mode=$3  ## for next docking: "SP / SF / SSF ..." See NAR_2016
interanchors=$4  ## for next docking. distance between the 2 anchors, in nucleotides
subanchorsfile=$5  ## results of previous docking
protein=$6 ## protein with the 2 anchors
targetdir=$7

anchornucl=1
if [ $mode = "SP" ] || [ $mode = "SF" ]; then
  anchornucl=3
  newfrag=$(($frag+1))
fi
newfrag=$(($frag+1))
if [ $mode = "SB" ] || [ $mode = "SA" ] ;then newfrag=$(($frag-1));fi

motif=`grep GP1 refe/frag${frag}r.pdb|awk '{print substr($4,length($4),1)}'| paste -sd ""`
pattern=proteincr-subanchor-frag${newfrag}-${mode}
tmp1=`mktemp`
tmp2=`mktemp`

# convert subanchors into coordinates
if [ "$Nsubanchors" = "all" ]; then
  Nsubanchors=`grep SEED $subanchorsfile|wc -l|awk '{print $1}'`
fi
$ATTRACTTOOLS/top $subanchorsfile $Nsubanchors > $tmp1

$ATTRACTDIR/collect $tmp1 /dev/null ${motif}/conf-1r.pdb  --ens 2 ${motif}-clust1A.list | \
  sed -e "s/   [0-9][0-9]   0.000/   99   0.000/g" > $tmp2

# create the protein-subanchor files (one per subanchor)
if [ ! -d $targetdir ]; then mkdir $targetdir; fi
cat /dev/null > $pattern.list
for i in `seq $Nsubanchors`; do
  cat $protein > $targetdir/$pattern-$i.pdb
  echo "$targetdir/$pattern-$i.pdb" >> $pattern.list
done
awk '$1=="MODEL"{j=$2}{if ($5=="2" || $5=="'$anchornucl'") print $0 >> "'$targetdir/$pattern'-" j ".pdb"}' $tmp2
