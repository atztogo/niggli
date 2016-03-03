.. _Niggli_cell:

Niggli cell
============

Usage of the code
------------------

The code is written in C and a python wrapper is prepared in
:file:`python` directory.
The C code is used to compile with your code. Usual library interface
is not prepared.
The python code is used as a module. To use this, ``numpy`` is required.

In both C and python codes, there are two input arguments, ``lattice``
and ``eps``. ``lattice`` is a ``double`` array with nine elements, 

.. math::

   (a_x, b_x, c_x, a_y, b_y, c_y, a_z, b_z, c_z).

In python, the input array will be fattened in the module. Therefore,
e.g., the following :math:`3\times 3` shape of a numpy array or a
python list is accepted:

.. math::

   \begin{pmatrix}
   a_x & b_x & c_x \\
   a_y & b_y & c_y \\
   a_z & b_z & c_z \\
   \end{pmatrix}.

The ``double`` variable of ``eps`` is used as the tolerance
parameter. The value should be much smaller than lattice parameters,
e.g., 1e-8. How it works is shown in the :ref:`following section
<niggli_algorithm>`.

Test
^^^^^

The test is found in :file:`python` directory as a python code. A set
of lattice parameters is found in :file:`lattices.dat` and the
references, which are the reduced lattice parameter made in the
version 0.1.1, are stored in :file:`reduced_lattices.dat`.

Example
^^^^^^^^

An example is found in :file:`python` directory as a python code.

.. _niggli_algorithm:

Algorithm to determine Niggli cell
-----------------------------------

Reference
^^^^^^^^^^

1. A Unified Algorithm for Determining the Reduced (Niggli) Cell,
   I. Krivý and B. Gruber, Acta Cryst., A32, 297-298 (1976)

2. The Relationship between Reduced Cells in a General Bravais lattice,
   B. Gruber, Acta Cryst., A29, 433-440 (1973)

3. Numerically stable algorithms for the computation of reduced unit cells,
   R. W. Grosse-Kunstleve, N. K. Sauter and P. D. Adams, Acta
   Cryst., A60, 1-6 (2004)
  

Algorithm
^^^^^^^^^^

Update variables
~~~~~~~~~~~~~~~~~~

The following variables used in this algorithm are initialized at the
beginning of the algorithm and updated at the every end of
A1-8 steps.

Define following variables as

.. math::

   &A = \mathbf{a}\cdot\mathbf{a}\\
   &B = \mathbf{b}\cdot\mathbf{b}\\ 
   &C = \mathbf{c}\cdot\mathbf{c}\\
   &\xi=2\mathbf{b}\cdot\mathbf{c}\\
   &\eta=2\mathbf{c}\cdot\mathbf{a}\\
   &\zeta=2\mathbf{a}\cdot\mathbf{b}.

They are elements of metric tensor where the off-diagonal elements are
doubled. Therefore the metric tensor :math:`\mathbf{G}` is represented as

.. math::

   \mathbf{G} =
   \begin{pmatrix}
   A & \zeta/2 & \eta/2 \\
   \zeta/2 & B & \xi/2 \\
   \eta/2 & \xi/2 & C
   \end{pmatrix}.
   
:math:`\xi`, :math:`\eta`, :math:`\zeta` are sorted by their ranges of
angles as shown below.

======= =====
Angle   value
======= =====
Acute   1
Obtuse  -1
Right   0
======= =====

These values are stored in variables :math:`l, m, n` as follows.

* Set initially :math:`l=m=n=0`.
* If :math:`\xi<-\varepsilon`, :math:`l=-1`.
* If :math:`\xi>\varepsilon`, :math:`l=1`. 
* If :math:`\eta<-\varepsilon`, :math:`m=-1`.
* If :math:`\eta>\varepsilon`, :math:`m=1`.
* If :math:`\zeta<-\varepsilon`, :math:`n=-1`.
* If :math:`\zeta>\varepsilon`, :math:`n=1`.

:math:`\mathbf{C}` found in each step is the transformation matrix
that is applied to basis vectors:

.. math::

   (\mathbf{a}', \mathbf{b}', \mathbf{c}') = (\mathbf{a}, \mathbf{b}, \mathbf{c})\mathbf{C}.

A1
~~

If :math:`A > B + \varepsilon` or
(:math:`\overline{|A-B|>\varepsilon}` and :math:`|\xi|>|\eta| + \varepsilon`),

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   0 & -1 & 0 \\
   -1 & 0 & 0 \\
   0 & 0 & -1 \\
   \end{pmatrix}.

A2
~~

If :math:`B > C + \varepsilon` or (:math:`\overline{|B-C|>\varepsilon}`
and :math:`|\eta|>|\zeta| + \varepsilon`),

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   -1 & 0 & 0 \\
   0 & 0 & -1 \\
   0 & -1 & 0 \\
   \end{pmatrix}.

Go to A1.

A3
~~

If :math:`lmn = 1`:

* :math:`i=-1` if :math:`l=-1` else :math:`i=1`
* :math:`j=-1` if :math:`m=-1` else :math:`j=1`
* :math:`k=-1` if :math:`n=-1` else :math:`k=1`

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   i & 0 & 0 \\
   0 & j & 0 \\
   0 & 0 & k \\
   \end{pmatrix}.

A4
~~

If :math:`l=-1`, :math:`m=-1`, and :math:`n=-1`, do nothing in A4.

If :math:`lmn = 0` or :math:`lmn = -1`:

Set :math:`i=j=k=1`. :math:`r` is used as a reference to :math:`i`,
:math:`j`, or :math:`k`, and is initially undefined.

* :math:`i=-1` if :math:`l=1`
* :math:`r\rightarrow i` if :math:`l=0`
* :math:`j=-1` if :math:`m=1`
* :math:`r\rightarrow j` if :math:`j=0`
* :math:`k=-1` if :math:`n=1`
* :math:`r\rightarrow k` if :math:`k=0`

If :math:`ijk=-1`:

*  :math:`i`, :math:`j`, or :math:`k` refered by :math:`r` is set to :math:`-1`.

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   i & 0 & 0 \\
   0 & j & 0 \\
   0 & 0 & k \\
   \end{pmatrix}.

A5
~~

If :math:`|\xi|>B + \varepsilon` or :math:`(\overline{|B - \xi| > \varepsilon}` and :math:`2\eta< \zeta
-\varepsilon)` or :math:`(\overline{|B + \xi| > \varepsilon}` and :math:`\zeta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & 0 \\
   0 & 1 & -\mathrm{sign}(\xi) \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A1.

A6
~~

If :math:`|\eta|>A + \varepsilon` or :math:`(\overline{|A - \eta| > \varepsilon}`
and :math:`2\xi < \zeta -\varepsilon)` or :math:`(\overline{|A + \eta| >
\varepsilon}` and :math:`\zeta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & -\mathrm{sign}(\eta) \\
   0 & 1 & 0 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A1.

A7
~~

If :math:`|\zeta|>A + \varepsilon` or :math:`(\overline{|A - \zeta| > \varepsilon},
2\xi < \eta -\varepsilon)` or :math:`(\overline{|A + \zeta| > \varepsilon}` and :math:`\eta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & -\mathrm{sign}(\zeta) & 0 \\
   0 & 1 & 0 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A1.

A8
~~

If :math:`\xi + \eta + \zeta + A + B < -\varepsilon` or :math:`(\overline{|\xi +
\eta + \zeta + A + B| > \varepsilon}` and :math:`2(A + \eta) + \zeta > \varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & 1 \\
   0 & 1 & 1 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A1.
