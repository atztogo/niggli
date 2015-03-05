#include "niggli.h"
#include <stdio.h>
#include <stdlib.h>

void show(double lattice[3][3])
{
  int i;
  for (i = 0; i < 3; i++) {
    printf("%f %f %f\n", lattice[i][0], lattice[i][1], lattice[i][2]);
  }
}

int main(void) {
  int i, j;
  double *metric;
  double lattice_1[3][3] = {
    {4, 0, 0},
    {1, 4, 0},
    {0, 0, 3}
  };

  double lattice_2[3][3] = {
    {  5.5089974077853840,  0.0000000000000000,  0.0000000000000000},
    { -2.3104709548280056,  6.6161727417255296,  0.0000000000000000},
    { -1.1044014154165944, -1.5396840484579815, 12.1086359754045372}
  };

  printf("Original\n");
  show(lattice_1);
  reduce((double*)lattice_1, 0.001);
  printf("Final\n");
  show(lattice_1);

  printf("Original\n");
  show(lattice_2);
  reduce((double*)lattice_2, 0.001);
  printf("Final\n");
  show(lattice_2);
  
}
