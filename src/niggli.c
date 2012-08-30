/* niggli.c */

#include <stdio.h>
#include <stdlib.h>
#include "niggli.h"

static double *
get_parameters(const double *lattice);

static double *
get_transpose(const double *lattice);

static double *
get_metric(const double *lattice);

static double *
multiply_matrices(const double *A, const double *B);

void
reduce(double *lattice, const double symprec)
{
  double *params = get_parameters(lattice);

  int i;
  for (i = 0; i < 6; i++) {
    printf("%f ", params[i]);
  }
  printf("\n");

  free(params);
}

static double *
get_parameters(const double *lattice)
{
  double *params = (double*)malloc(sizeof(double) * 6);
  double *metric = get_metric(lattice);

  params[0] = metric[0];
  params[1] = metric[4];
  params[2] = metric[8];
  params[3] = metric[5] * 2;
  params[4] = metric[2] * 2;
  params[5] = metric[1] * 2;
  return params;
}

static double *
get_transpose(const double *lattice)
{
  int i, j;
  double *transpose = (double*)malloc(sizeof(double) * 9);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      transpose[i * 3 + j] = lattice[j * 3 + i];
    }
  }
  return transpose;
}

static double *
get_metric(const double *lattice)
{
  double *metric;
  double *lattice_T = get_transpose(lattice);

  metric = multiply_matrices(lattice, lattice_T);
  free(lattice_T);
  return metric;
}

static double *
multiply_matrices(const double *A, const double *B)
{
  int i, j, k;
  double *C = (double*)malloc(sizeof(double) * 9);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      C[i * 3 + j] = 0;
      for (k = 0; k < 3; k++) {
	C[i * 3 + j] += A[i * 3 + k] * B[k * 3 + j];
      }
    }
  }
  return C;
}
