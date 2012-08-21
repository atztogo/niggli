/* niggli.c */

#include <stdio.h>
#include <stdlib.h>
#include "niggli.h"

static int step1(int C[9])
{
  int i, j;

  for (i = 0; i < 9; i++) {
    C[i] = 0;
  }
}
		 
ngl_matrix * alloc_matrix(const ngl_vtype ngl_vtype,
			  const int m,
			  const int n)
{
  ngl_matrix * matrix;

  matrix = (ngl_matrix *)malloc(sizeof(ngl_matrix));
  if (matrix == NULL) goto ret;
  matrix->m = m;
  matrix->n = n;

  switch (ngl_vtype) {
  case NGL_INT:
    matrix->ngl_vtype = ngl_vtype;
    matrix->p = (void *)malloc(sizeof(double) * m * n);
    break;
  case NGL_DOUBLE:
    matrix->ngl_vtype = ngl_vtype;
    matrix->p = (void *)malloc(sizeof(int) * m * n);
    break;
  default:
    free(matrix);
    matrix = NULL;
    goto ret;
  }

  if (matrix->p == NULL) {
    free(matrix);
    matrix = NULL;
  }
  
 ret:
  return matrix;
}

void free_matrix(ngl_matrix * matrix) {
  if (matrix == NULL) goto ret;
  if (matrix->p == NULL) {
    free(matrix);
    goto ret;
  }
  free(matrix->p);
  free(matrix);
 ret:
  ;
}

void ngl_set_matrix_INT(ngl_matrix * matrix,
			const int i,
			const int j,
			const int v)
{
  int * p;
  p = (int *)matrix->p;
  p[i * matrix->n + j] = v;
}

void ngl_set_matrix_DBL(ngl_matrix * matrix,
			const int i,
			const int j,
			const double v)
{
  double * p;
  p = (double *)matrix->p;
  p[i * matrix->n + j] = v;
}

void reduce_lattice(double lattice[3][3],
		    const double symprec)
{
  ;
}
