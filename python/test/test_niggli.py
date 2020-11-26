import numpy as np
from niggli import niggli_reduce


def test_reference_data(test_data):
    input_lattices, reference_lattices = test_data
    for i, reference_lattice in enumerate(reference_lattices):
        angles = np.array(_get_angles(reference_lattice))
        all_acute = (angles < 90 + 1e-3).all()
        all_nonacute = (angles > 90 - 1e-3).all()
        assert all_acute or all_nonacute, ("%d %s" % (i + 1, angles))


def test_niggli_reduce(test_data):
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


def _get_lattice_parameters(lattice):
    return np.sqrt(np.dot(lattice.T, lattice).diagonal())


def _get_angles(lattice):
    a, b, c = _get_lattice_parameters(lattice)
    alpha = np.arccos(np.vdot(lattice[:, 1], lattice[:, 2]) / b / c)
    beta = np.arccos(np.vdot(lattice[:, 2], lattice[:, 0]) / c / a)
    gamma = np.arccos(np.vdot(lattice[:, 0], lattice[:, 1]) / a / b)
    return np.array([alpha, beta, gamma]) / np.pi * 180


def _show_lattice(i, lattice):
    print("# %d" % (i + 1))
    for v in lattice.T:
        print(" ".join(["%20.16f" % x for x in v]))
