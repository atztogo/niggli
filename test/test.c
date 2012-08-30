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
  double lattice[3][3] = {
    {4, 0, 0},
    {1, 4, 0},
    {0, 0, 3}
  };

  show(lattice);
  reduce(lattice, 0.001);
  show(lattice);
}
