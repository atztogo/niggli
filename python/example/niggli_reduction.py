#!/usr/bin/env python

import numpy as np
from niggli import niggli_reduce, get_version

def get_lattice_parameters(lattice):
    return np.sqrt(np.dot(lattice.T, lattice).diagonal())

def get_angles(lattice):
    a, b, c = get_lattice_parameters(lattice)
    alpha = np.arccos(np.vdot(lattice[:,1], lattice[:,2]) / b / c)
    beta  = np.arccos(np.vdot(lattice[:,2], lattice[:,0]) / c / a)
    gamma = np.arccos(np.vdot(lattice[:,0], lattice[:,1]) / a / b)
    return np.array([alpha, beta, gamma]) / np.pi * 180

def lattice2cartesian(a, b, c, alpha, beta, gamma):
    """
    The conversion refers the wikipedia,
    http://en.wikipedia.org/wiki/Fractional_coordinates
    """
    cg = np.cos(gamma / 180 * np.pi)
    cb = np.cos(beta / 180 * np.pi)
    ca = np.cos(alpha / 180 * np.pi)
    sg = np.sin(gamma / 180 * np.pi)
    L = np.zeros((3, 3))
    L[0, 0] = a
    L[0, 1] = b * cg
    L[0, 2] = c * cb
    L[1, 1] = b * sg
    L[1, 2] = c * (ca - cb * cg) / sg
    L[2, 2] = c * np.sqrt(1 - ca ** 2 - cb ** 2 - cg ** 2 +
                          2 * ca * cb * cg) / sg
    return L

def show_lattice(lattice):
    for v, axis in zip(lattice.T, ('a', 'b', 'c')):
        print("%s %s" % (axis, v))
    print("Lengths %s" % get_lattice_parameters(lattice))
    print("Angles %s" % np.array(get_angles(lattice)))
    print("V %f" % np.linalg.det(lattice))


if __name__ == '__main__':
    print("Version %d.%d.%d" % get_version())

    # Example in the paper by Krivy & Gruber 1976 
    a, b, c = np.sqrt([9, 27, 4])
    alpha = np.arccos(-5 / (2 * b * c)) / np.pi * 180
    beta = np.arccos(-4 / (2 * a * c)) / np.pi * 180
    gamma = np.arccos(-22 / (2 * a * b)) / np.pi * 180

    lattice = lattice2cartesian(a, b, c, alpha, beta, gamma)
    reduced_lattice = niggli_reduce(lattice, eps=1e-5)
    
    print("Original:")
    show_lattice(lattice)
    
    print("Reduced:")
    show_lattice(reduced_lattice)
