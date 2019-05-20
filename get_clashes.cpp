/*#include "omp.h"*/
void get_clashes(
  int n, int nat, float threshold,
  double *structures, bool *matrix
)

{
  /*#pragma omp parallel for schedule(static,4)*/
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
      bool clash = 0;
      for (int nr1 = 0; nr1 < nat; nr1++){
        int off1 = i*nat*3 + nr1*3;
        double *at1 = structures+off1;
        for (int nr2 = 0; nr2 < nat; nr2++){
          int off2 = j*nat*3 + nr2*3;
          double *at2 = structures+off2;
          double dist = 0;
          for (int x = 0; x < 3; x++){
            dist += (at1[x] - at2[x])*(at1[x] - at2[x]);
          }
          if (dist < threshold){
            matrix[i*n + j] = 1;
            matrix[j*n + i] = 1;
            clash = 1;
            break;
          }
        }
        if (clash){
          break;
        }        
      }
    }
  }
}
