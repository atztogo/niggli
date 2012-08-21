#include "niggli.h"

int main(void) {
  int i, j;
  ngl_matrix * matrix;

  matrix = alloc_matrix(NGL_INT, 3, 3);
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      ngl_set_matrix_INT(matrix, i, j, i * 3 + j);
    }
  }

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      ngl_set_matrix_INT(matrix, i, j, i * 3 + j);
    }
  }

  free_matrix(matrix);
}
