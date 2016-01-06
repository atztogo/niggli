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

def show_lattice(lattice):
    for v, axis in zip(lattice.T, ('a', 'b', 'c')):
        print("%s %s" % (axis, v))
    print("Lengths %s" % get_lattice_parameters(lattice))
    print("Angles %s" % np.array(get_angles(lattice)))
    print("V %f" % np.linalg.det(lattice))

lattice_str = """
 -3.0399837305035393   0.2689430591255473  -0.3854696358687387
  0.5019497901415106   1.1955705707455986   9.1769697990207320
  2.3242680883263844   8.9135745201241541   0.1859370039210433
"""

print("Version %d.%d.%d" % get_version())

print("Original:")
lattice = np.reshape([float(x) for x in lattice_str.strip().split()], (3, 3)).T
show_lattice(lattice)

print("Reduced:")
reduced_lattice = niggli_reduce(lattice, eps=1e-5)
show_lattice(reduced_lattice)
