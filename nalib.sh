#run this from the data directory!
pdbcodes=$1
na=$2
export NAFRAG=/home/isaure/Scripts/nafrag
export ATTRACTTOOLS=/home/isaure/git-attract/tools
export ATTRACTDIR=/home/isaure/git-attract/bin
d=`pwd`

rd=R
ut=U
if [ "$na" == "dna" ];then
  ut=T
  rd=D
fi
echo $ut $rd

set -u -e
#if false;then
###############################################################
echo "---------------------------- Downloading PDBs"
###############################################################
if [ ! -d brutPDBs ];then mkdir brutPDBs; fi
cd brutPDBs
for i in `cat ../$pdbcodes|awk '{print toupper($0)}'`; do
    #if [ ! -s $i.pdb ] && [ ! -s $i.pdb.bz2 ] && [ ! -s ../interface/$i-1.pdb ];then
    if [ ! -s $i.pdb ] && [ ! -s $i.pdb.bz2 ] ;then
      echo "downloading $i"
      pdb_download $i > /dev/null 2> /dev/null
      sed -i 's/SE   MSE/ SD  MSE/' $i.pdb
      sed -i 's/MSE/MET/' $i.pdb
    elif [ -s $i.pdb.bz2 ];then
      if [ 1 -gt $(ls  ./cleanPDB/${i}[A-Z]-1.pdb 2>/dev/null | wc -w) ]; then
        bunzip2 $i.pdb.bz2
      fi
    fi
done
cd $d
mkdir -p chainsmodels/
mkdir -p cleanPDB/
mkdir -p interface/
mkdir -p 3dna/
mkdir -p backup
#mv chainsmodels*.json backup/
##########################################################################
echo "-------------------------- check_pdb.py"
##########################################################################
$NAFRAG/check_pdb.py brutPDBs/ $pdbcodes corrupted_pdb_files.list \
  tofix.list checked.list splitted.list $ATTRACTDIR/../allatom/$na-mutate.list \
   $na > log
sort -u checked.list > bi; mv bi checked.list
##########################################################################
echo "-------------------------- interface_pdb_contacts.py"
##########################################################################
  #Split into chains and models. Creates:
  #   chainsmodels/xxxxX-y.pdb
  #   chainsmodels.json
  #!!! delete pdb if already present in chainsmodels.json !!
python3 $NAFRAG/interface_pdb_contacts.py 5 brutPDBs chainsmodels checked.list \
  $ATTRACTTOOLS/../allatom/$na-mutate.list chainsmodels.json $na --delete \
   > interface_pdb_contacts.log

##########################################################################
echo "--------------------------------- clean_rna.py"
##########################################################################
  ### Remove/rename atoms from modified bases. Creates:
      #   cleanPDB/xxxxX-y.pdb
      #   cleanPDB.list
  # Also checks that every chain has " " or "A" in column 17 (alternative conformations)
  # TODO: remove clashing atoms
$NAFRAG/clean_rna.py 'chainsmodels/' 'cleanPDB/' cleanPDB.list \
  $ATTRACTDIR/../allatom/$na-mutate.list chainsmodels.json \
  clean_rna.json $na --delete > clean.err

##########################################################################
echo "---------------------------------parse_pdb_initial.sh"
##########################################################################
  ### Applies aareduce to remove non-RNA. Creates:
  #    parse_pdb_initial.errors
  #    cleanPDB/xxxxX-y-iniparse.pdb
  # marks missing atoms by XXX coordinates
$NAFRAG/parse_pdb_initial.sh cleanPDB.list $na >> clean-iniparse.list
sort -u clean-iniparse.list > bi; mv bi clean-iniparse.list

##########################################################################
#echo "--------------------------------- build monolib"
##########################################################################
#$NAFRAG/build_monolib.py templates clean-iniparse.list monolib
#for a in A C G $ut ; do
#  cluster_monolib.sh monolib/$rd$a-fit.npy 0.3 templates/$rd$a.pdb
#done

##########################################################################
echo "---------------------------------excise-pdb-missings.py"
##########################################################################
  ### Records nucl with missing atoms. Creates
      #    excise-pdb-missings.err
      #    excised.list  : List of files checked for missing atoms
      #                     Some chains are discarded
  ### Adds entries in chainsmodels.json:
      #   'missings' : res with missing atoms (7 => deleted)
      #   'sequence'
python3 $NAFRAG/excise-pdb-missings.py cleanPDB clean_rna.json excise.json \
  excised.list  $na --delete

#gawk 'ARGIND==1{failed[$1] == 1} '
#TODO : remove deleted residues from previous json
##########################################################################
echo "---------------------------------parse_pdb-missings"
##########################################################################
  ### Fill-up missing atoms
      #    creates: _ parse_pdb.errors
      #             _ cleanPDB/xxxxxX-y-iniparse-aa.pdb
      #             _ clean-iniparse-aa.list
      #             _ still_missing.list
      # Some 5PHO can still be missing because all conf in nalib clash
      # Those are written as XXX, and should be indicated in a json file
$NAFRAG/parse_pdb-missings.sh excised.list $na

# retrieve missing (always clashing) 5PHO
#TODO: remove chain/struct if <3 nucl left
python3 $NAFRAG/excise-still-missing.py cleanPDB still_missing.list \
  clean-iniparse-aa.list excise.json $na
sort -u clean-iniparse-aa.list > bi; mv bi clean-iniparse-aa.list
##########################################################################
echo "---------------------------------3dna"
##########################################################################
  ###concatenate protein and RNA chains for each model###
mkdir -p 3dna
$NAFRAG/3dna.py excise.json $NAFRAG/3dna.sh
$NAFRAG/3dna_parse_json.py excise.json x3dna.json $na

##########################################################################
echo "---------------------------------parse_pdb_AC"
##########################################################################
  ### Mutate G -> A and U-> C ###
if [ ! -d  templates ];then
  ln -s ~/templates/$na templates
fi
$NAFRAG/parse_pdb_AC.sh clean-iniparse-aa.list $na >> pdbfiles-AC.list
sort -u pdbfiles-AC.list > bi; mv bi pdbfiles-AC.list
# Normally, check parse_pdb_AC.errors (should contain no errors)
# Activate the line below only for testing
#for i in `cat pdbfiles-AC.list`; do touch $i ; done
exit
#pdbfiles-AC.list
rm -rf PDBs; mkdir PDBs
##########################################################################
echo "---------------------------------fragmt-from-AC"
##########################################################################
$NAFRAG/fragmt-from-AC.py x3dna.json fragments_ori.json $na listofseq 'cleanPDB'
mkdir -p trilib
cd trilib
ln -sf ../fragments_ori.json
mkdir -p PDBss
if [ ! -d  templates ];then
  ln -s ~/templates/$na templates
fi
##########################################################################
echo "------------------- fragmt clustering"
##########################################################################
cat /dev/null > mutated.list
# Clustering
for a in A C; do for b in A C ; do for c in A C; do
  m=$a$b$c
  echo $m
  echo $m >> mutated.list
  $NAFRAG/clusterfrag_npy.sh $m > clusterfrag_npy-$m.log &
done;done;done
wait

for a in A C; do for b in A C ; do for c in A C; do
  m=$a$b$c
  $NAFRAG/create_libraries.sh $m
done

python $NAFRAG/assign_clusters.py fragments_ori.json $na \
 "dr0.2.list" "fit-dr0.2r-clust1.0" "fit-dr0.2r-clust2.0" fragments_clust.json "aa"

python $NAFRAG/assign_clusters.py fragments_ori_clust.json $na \
 "C246-clust0.2" "C246-clust1.0" "C246-clust1.0-clust2.0" fragments_clust.json "aa"

##########################################################################
echo "--------------------- create_alternative_conformers"
##########################################################################
$NAFRAG/create_alternative_conformer.sh $na

exit

#for a in A C; do for b in A C ; do for c in A C; do
#    m=$a$b$c
#    echo "clustering $m at 2.0 A"
#    $NAFRAG/clusterfrag_npy.sh $m > clusterfrag_npy-$m.log &
#done;done;done
#wait

$NAFRAG/mutate-AC-libraries_npy.py $na

# Creates fragments_demut.json
$NAFRAG/demutate.sh mutated.list

#$NAFRAG/copy-trilib.sh ../trilib
