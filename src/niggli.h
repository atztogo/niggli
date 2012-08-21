/* niggli.h */
#ifndef __NIGGLI_H__
#define __NIGGLI_H__

typedef enum ngl_vtype {
  NGL_INT = 0,
  NGL_DOUBLE
} ngl_vtype;

typedef struct ngl_matrix {
  void *p;
  ngl_vtype ngl_vtype;
  int m;
  int n;
} ngl_matrix;

ngl_matrix * ngl_alloc_matrix(const ngl_vtype ngl_vtype,
			      const int m,
			      const int n);
void ngl_free_matrix(ngl_matrix * matrix);
void ngl_set_matrix_INT(ngl_matrix * matrix,
			const int i,
			const int j,
			const int v);
void ngl_set_matrix_DBL(ngl_matrix * matrix,
			const int i,
			const int j,
			const double v);
int ngl_get_matrix_INT(ngl_matrix * matrix,
		       const int i,
		       const int j);
double ngl_get_matrix_DBL(ngl_matrix * matrix,
			  const int i,
			  const int j);
void reduce_lattice(double lattice[3][3],
		    const double symprec);

#endif
