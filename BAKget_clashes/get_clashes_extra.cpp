typedef int Pair[2];

/*#include "omp.h"*/
/* structures = np.array of poses coordinates
      !!! they do not have all the same number of atoms,
      !!! So set the nat to the maximal nat of all structures
   pairs = pairs of structure indices to be checked
   npairs = Nb of pairs
   maxnat = maximum number of atom in structures
   nat = list of number of atoms in each structure
   threshold = cutoff**2 for clash, in Angstrom**2
   result = indices of clashing pairs in the list "pairs"
*/
int get_clashes_extra(
  double *structures, Pair *pairs,
  int npairs, int *nat, int maxnat, float threshold,
  int *result
)

{
  /*#pragma omp parallel for schedule(static,4)*/
  int count = 0;
  for (int p = 0; p < npairs; p++){
    bool clash = 0;
    int p1 = pairs[p][0];
    int p2 = pairs[p][1];
    for (int at1 = 0; at1 < nat[p1]; at1++){
      double *coor1 = structures + p1*maxnat*3 + at1*3;
      for (int at2 = 0; at2 < nat[p2]; at2++){
        double *coor2 = structures + p2*maxnat*3 + at2*3;
        double dist = 0;
        for (int x = 0; x < 3; x++){
          dist += (coor1[x] - coor2[x])*(coor1[x] - coor2[x]);
        }
        if (dist < threshold){
          clash = 1;
          break;
        }
      }
      if (clash){
        break;
      }
    }
    if (clash){
      result[count] = p;
      count++;
    }
  }
  return count;
}
