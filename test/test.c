#include "niggli.h"
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <math.h>

/* np.savetxt("lattice_ravel.dat", np.loadtxt("lattices.dat").ravel()) */

static int run_test(FILE *fptr);


int main(void)
{
  int succeeded;
  FILE *fptr;

  succeeded = 0;

  fptr = fopen("lattice_ravel.dat", "r");
  if (fptr == NULL) {
    printf("File could not be opened.");
    return 1;
  }
  run_test(fptr);
  fclose(fptr);

  fptr = fopen("lattice_large_L_ravel.dat", "r");
  if (fptr == NULL) {
    printf("File could not be opened.");
    return 1;
  }
  run_test(fptr);
  fclose(fptr);

  return succeeded;
}

static int run_test(FILE *fptr)
{
  int i, j, succeeded, nlat;
  char * line = NULL;
  size_t len = 0;
  ssize_t read;
  double eps;
  double lat[9];

  succeeded = 0;
  eps = 1e-5;
  nlat = 783;

  for (i = 0; i < nlat; i++) {
    printf("lattice %d: ", (i + 1));
    for (j = 0; j < 9; j++) {
      read = getline(&line, &len, fptr);
      lat[j] = atof(line);
      printf("%f ", lat[j]);
    }
    printf("\n");
    if (!niggli_reduce(lat, eps)) {
      succeeded = 1;
    }
  }

  return succeeded;
}
