# Copyright (C) 2016 Atsushi Togo
# All rights reserved.
#
# This file is part of niggli
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the niggli project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from . import _niggli as niggli
import numpy as np

def get_version():
    return tuple(niggli.version())

def niggli_reduce(lattice, eps=1e-5):
    """Run Niggli reduction

    Args:
        lattice: Lattice parameters
            [a_x, b_x, c_x, a_y, b_y, c_y, a_z, b_z, c_z] or
            [[a_x, b_x, c_x], [a_y, b_y, c_y], [a_z, b_z, c_z]]
        eps: Tolerance.
    
    Returns:
        Reduced lattice parameters
            [[a_x, b_x, c_x], [a_y, b_y, c_y], [a_z, b_z, c_z]]
    """
    reduced_lattice = np.array(np.ravel(lattice), dtype='double')
    result = niggli.niggli_reduce(reduced_lattice, float(eps))
    if result == 0:
        return None
    else:
        return np.reshape(reduced_lattice, (3, 3), order='C')

