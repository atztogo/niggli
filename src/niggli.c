/* niggli.c */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "niggli.h"

static double A, B, C, eta, xi, zeta, eps;
static int l, m, n;
static double *tmat = NULL;
static double *lattice = NULL;

static void
show(void);

static void
initialize(const double *lattice_, const double eps_);

static void
finalize(double *lattice_);

static void
reset(void);

static void
step0(void);

static int
step1(void);

static int
step2(void);

static int
step3(void);

static int
step4(void);

static void
set_parameters(void);

static void
set_angle_types(void);

static double *
get_transpose(const double *M);

static double *
get_metric(const double *M);

static double *
multiply_matrices(const double *A, const double *B);

static void
show(void)
{
  int i;
  printf("%f %f %f %f %f %f\n", A, B, C, xi, eta, zeta);
  printf("%d %d %d\n", l, m, n);
  
  for (i = 0; i < 3; i++) {
    printf("%f %f %f\n", lattice[i * 3], lattice[i * 3 + 1], lattice[i * 3 + 2]);
  }
  
}

void
reduce(double *lattice_, const double eps_)
{
  int i;

  initialize(lattice_, eps_);
  step0();
  show();
  
  for (i = 0; i < 10; i++) {
    if (step1()) {
      printf("step1\n");
      show();
      printf("\n");
    }

    if (step2()) {
      printf("step2\n");
      show();
      printf("\n");
      continue;
    }

    if (step3()) {
      printf("step3\n");
      show();
      printf("\n");
    }

    if (step4()) {
      printf("step4\n");
      show();
      printf("\n");
    }
  }

  finalize(lattice_);
}

static void
initialize(const double *lattice_, const double eps_)
{
  tmat = (double*)malloc(sizeof(double) * 9);
  eps = eps_;
  lattice = (double*)malloc(sizeof(double) * 9);
  memcpy(lattice, lattice_, sizeof(double) * 9);
}

static void
finalize(double *lattice_)
{
  free(tmat);
  memcpy(lattice_, lattice, sizeof(double) * 9);
  free(lattice);
}

static void
reset(void)
{
  double *lat_tmp = multiply_matrices(lattice, tmat);
  memcpy(lattice, lat_tmp, sizeof(double) * 9);
  step0();
  free(lat_tmp);
}

static void
step0(void)
{
  set_parameters();
  set_angle_types();
}

static int
step1(void)
{
  if (A > B - eps ||
      fabs(A -B) < eps && fabs(xi) > fabs(eta) - eps) {
    tmat[0] = 0,  tmat[1] = -1, tmat[2] = 0;
    tmat[3] = -1, tmat[4] = 0,  tmat[5] = 0;
    tmat[6] = 0,  tmat[7] = 0,  tmat[8] = -1;
    reset();
    return 1;
  }
  else {return 0;}
}

static int
step2(void)
{
  if (B > C - eps ||
      fabs(B - C) < eps && fabs(eta) > fabs(zeta) - eps) {
    tmat[0] = -1, tmat[1] = 0,  tmat[2] = 0;
    tmat[3] = 0,  tmat[4] = 0,  tmat[5] = -1;
    tmat[6] = 0,  tmat[7] = -1, tmat[8] = 0;
    reset();
    return 1;
  }
  else {return 0;}
}

static int
step3(void)
{
  int i, j, k;
  if (l * m * n == 1) {
    if (l == -1) {i = -1;} else {i = 1;}
    if (m == -1) {j = -1;} else {j = 1;}
    if (n == -1) {k = -1;} else {k = 1;}
    tmat[0] = i, tmat[1] = 0, tmat[2] = 0;
    tmat[3] = 0, tmat[4] = j, tmat[5] = 0;
    tmat[6] = 0, tmat[7] = 0, tmat[8] = k;
    reset();
    return 1;
  }
  else {return 0;}
}

static int
step4(void)
{
  int i, j, k;
  if (l * m * n == 0 || l * m * n == -1) {
    if (l == -1) {i = -1;} else {i = 1;}
    if (m == -1) {j = -1;} else {j = 1;}
    if (n == -1) {k = -1;} else {k = 1;}

    if (i * j * k == -1) {
      if (l == 0) {i = -1;}
      if (m == 0) {j = -1;}
      if (n == 0) {k = -1;}
    }
    
    tmat[0] = i, tmat[1] = 0, tmat[2] = 0;
    tmat[3] = 0, tmat[4] = j, tmat[5] = 0;
    tmat[6] = 0, tmat[7] = 0, tmat[8] = k;
    reset();
    return 1;
  }
  else {return 0;}
}

static void
set_angle_types(void)
{
  l = 0, m = 0, n = 0;
  if (xi < -eps) {l = -1;}
  if (xi > eps) {l = 1;}
  if (eta < -eps) {m = -1;}
  if (eta > eps) {m = 1;}
  if (zeta < -eps) {n = -1;}
  if (zeta > eps) {n = 1;}
}

static void
set_parameters(void)
{
  double *G = get_metric(lattice);

  A = G[0];
  B = G[4];
  C = G[8];
  xi = G[5] * 2;
  eta = G[2] * 2;
  zeta = G[1] * 2;

  free(G);
}

static double *
get_transpose(const double *M)
{
  int i, j;
  double *M_T = (double*)malloc(sizeof(double) * 9);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      M_T[i * 3 + j] = M[j * 3 + i];
    }
  }
  return M_T;
}

static double *
get_metric(const double *M)
{
  double *G;
  double *M_T = get_transpose(M);

  G = multiply_matrices(M_T, M);

  free(M_T);
  return G;
}

static double *
multiply_matrices(const double *L, const double *R)
{
  int i, j, k;
  double *M = (double*)malloc(sizeof(double) * 9);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      M[i * 3 + j] = 0;
      for (k = 0; k < 3; k++) {
	M[i * 3 + j] += L[i * 3 + k] * R[k * 3 + j];
      }
    }
  }
  return M;
}
