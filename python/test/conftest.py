import os
import pytest
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session')
def test_data():
    input_lattices = _read_file(
        os.path.join(current_dir, "lattices.dat"))
    reference_lattices = _read_file(
        os.path.join(current_dir, "reduced_lattices.dat"))
    return input_lattices, reference_lattices


def _read_file(filename):
    all_lattices = []
    with open(filename) as f:
        lattice = []
        for line in f:
            if line[0] == '#':
                continue
            lattice.append([float(x) for x in line.split()])
            if len(lattice) == 3:
                all_lattices.append(np.transpose(lattice))
                lattice = []
    return all_lattices
