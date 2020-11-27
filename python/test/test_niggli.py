import numpy as np
from niggli import niggli_reduce


tmat_U = [[1, 1, 2], [0, 1, 3], [0, 0, 1]]
tmat_L = [[1, 0, 0], [1, 1, 0], [2, 3, 1]]
tmat_small_L = [[1, -18, 25], [0, 1, 15], [0, 0, 1]]
tmat_small_U = [[1, 0, 0], [15, 1, 0], [-18, 25, 1]]
tmat_large_L = [[1, 0, 0], [1500, 1, 0], [-180, 250, 1]]
tmat_large_U = [[1, -180, 250], [0, 1, 1500], [0, 0, 1]]


def test_reference_data(test_data):
    input_lattices, reference_lattices = test_data
    for i, reference_lattice in enumerate(reference_lattices):
        all_acute, all_nonacute, angles = _get_angle_types(reference_lattice)
        assert all_acute or all_nonacute, ("%d %s" % (i + 1, angles))


def test_niggli_reduce(test_data):
    """

    This test assumes no fallback to Delaunay reduction.
    Change of the following number in `src/niggli.c` may result in
    different output basis vectors:

        #define NIGGLI_MAX_NUM_LOOP 10000

    See how the fallback works at 'niggli_reduce' in src/niggli.c.

    """

    input_lattices, reference_lattices = test_data
    for i, (input_lattice, reference_lattice) in enumerate(
            zip(input_lattices, reference_lattices)):
        reduced_lattice = niggli_reduce(input_lattice)
        # _show_lattice(i, reduced_lattice)

        np.testing.assert_allclose(
            reduced_lattice, reference_lattice,
            err_msg="\n".join(
                ["# %d" % (i + 1),
                 "Input lattice",
                 "%s" % input_lattice,
                 " angles: %s" % np.array(_get_angles(input_lattice)),
                 "Reduced lattice in reference data",
                 "%s" % reference_lattice,
                 " angles: %s" % np.array(_get_angles(reference_lattice)),
                 "Reduced lattice",
                 "%s" % reduced_lattice,
                 " angles: %s" % np.array(_get_angles(reduced_lattice))]))


def test_niggli_reduce_for_modified_lattices(test_data):
    """

    This test should work even when fallback to Delaunay reduction happens.
    See docstring of `test_niggli_reduce` about the fallback to Delaunay
    reduction.

    """

    input_lattices, reference_lattices = test_data

    for tmat in (
            tmat_U, tmat_L, np.dot(tmat_U, tmat_L),
            tmat_small_U, tmat_small_L, np.dot(tmat_small_U, tmat_small_L),
            tmat_large_U, tmat_large_L):
        for i, (input_lattice, reference_lattice) in enumerate(
                zip(input_lattices, reference_lattices)):
            mod_lattice = _modify_lattice(input_lattice, tmat)
            reduced_lattice = niggli_reduce(mod_lattice)
            lengths = np.sort(_get_lattice_parameters(reduced_lattice))
            lengths_ref = np.sort(_get_lattice_parameters(reference_lattice))

            np.testing.assert_allclose(
                lengths, lengths_ref,
                err_msg="\n".join(
                    ["# %d" % (i + 1),
                     "Input lattice (modified)",
                     "%s" % input_lattice,
                     " angles: %s" % np.array(_get_angles(mod_lattice)),
                     "Reduced lattice in reference data",
                     "%s" % reference_lattice,
                     " angles: %s" % np.array(_get_angles(reference_lattice)),
                     "Reduced lattice",
                     "%s" % reduced_lattice,
                     " angles: %s" % np.array(_get_angles(reduced_lattice))]))


def _modify_lattice(lattice, tmat):
    mod_lattice = np.dot(lattice, tmat)
    assert abs(np.linalg.det(mod_lattice) - np.linalg.det(lattice)) < 1e-5
    return mod_lattice


def _get_lattice_parameters(lattice):
    return np.sqrt(np.dot(np.transpose(lattice), lattice).diagonal())


def _get_angles(lattice):
    a, b, c = _get_lattice_parameters(lattice)
    alpha = np.arccos(np.vdot(lattice[:, 1], lattice[:, 2]) / b / c)
    beta = np.arccos(np.vdot(lattice[:, 2], lattice[:, 0]) / c / a)
    gamma = np.arccos(np.vdot(lattice[:, 0], lattice[:, 1]) / a / b)
    return np.array([alpha, beta, gamma]) / np.pi * 180


def _get_angle_types(lattice):
    angles = np.array(_get_angles(lattice))
    all_acute = (angles < 90 + 1e-3).all()
    all_nonacute = (angles > 90 - 1e-3).all()
    return all_acute, all_nonacute, angles


def _show_lattice(i, lattice):
    print("# %d" % (i + 1))
    for v in lattice.T:
        print(" ".join(["%20.16f" % x for x in v]))


if __name__ == '__main__':
    """Produce data file for C test


    """

    data = np.loadtxt("lattices.dat").reshape(-1, 3, 3)
    np.savetxt("lattice_ravel.dat", data.ravel())
    np.savetxt("lattice_large_L_ravel.dat", np.dot(data, tmat_large_L).ravel())
