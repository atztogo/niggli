#include "niggli.h"
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  int i, j;
  double *metric;
  double lattice[3][3] = {
    {4, 0, 0},
    {1, 4, 0},
    {0, 0, 3}
  };

  reduce(lattice, 0);
}
