.. _Niggli_cell:

Niggli cell
============

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

A0
~~

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
   \eta/2 & \xi/2 & B
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

* Set initially :math:`l=m=l=0`.
* If :math:`\xi<-\varepsilon`, :math:`l=-1`.
* If :math:`\xi>\varepsilon`, :math:`l=1`. 
* If :math:`\eta<-\varepsilon`, :math:`m=-1`.
* If :math:`\eta>\varepsilon`, :math:`m=1`.
* If :math:`\zeta<-\varepsilon`, :math:`n=-1`.
* If :math:`\zeta>\varepsilon`, :math:`n=1`.


A1
~~

If :math:`A>B - \varepsilon` or
(:math:`|A-B|\le\varepsilon` and :math:`|\xi|>|\eta| - \varepsilon`),

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   0 & -1 & 0 \\
   -1 & 0 & 0 \\
   0 & 0 & -1 \\
   \end{pmatrix}.

A2
~~

If :math:`B>C-\varepsilon` or (:math:`|B-C|\le\varepsilon`
and :math:`|\eta|>|\zeta| - \varepsilon`),

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   -1 & 0 & 0 \\
   0 & 0 & -1 \\
   0 & -1 & 0 \\
   \end{pmatrix}.

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

If :math:`lmn = 0` or :math:`lmn = -1`:

* :math:`i=-1` if :math:`l=1` else :math:`i=1`
* :math:`j=-1` if :math:`m=1` else :math:`j=1`
* :math:`k=-1` if :math:`n=1` else :math:`k=1`

If :math:`ijk=-1`, then overwrite :math:`i,j,k`:

* :math:`i=-1` if :math:`l=0`
* :math:`j=-1` if :math:`m=0`
* :math:`k=-1` if :math:`n=0`

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   i & 0 & 0 \\
   0 & j & 0 \\
   0 & 0 & k \\
   \end{pmatrix}.

A5
~~

If :math:`|\xi|>B + \varepsilon` or :math:`(|B - \xi| < \varepsilon, 2\eta< \zeta
-\varepsilon)` or :math:`(|B + \xi| < \varepsilon, \zeta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & 0 \\
   0 & 1 & -\mathrm{sign}(\xi) \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A0.

A6
~~

If :math:`|\eta|>A + \varepsilon` or :math:`(|A - \eta| < \varepsilon,
2\xi < \zeta -\varepsilon)` or :math:`(|A + \eta| < \varepsilon, \zeta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & -\mathrm{sign}(\eta) \\
   0 & 1 & 0 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A0.

A7
~~

If :math:`|\zeta|>A + \varepsilon` or :math:`(|A - \zeta| < \varepsilon,
2\xi < \eta -\varepsilon)` or :math:`(|A + \zeta| < \varepsilon, \eta< -\varepsilon)`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & -\mathrm{sign}(\zeta) & 0 \\
   0 & 1 & 0 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A0.

A8
~~

If :math:`\xi + \eta + \zeta + A + B < -\varepsilon` or :math:`[\xi +
\eta + \zeta + A + B = 0, 2(A + \eta) + \zeta > \varepsilon]`:

.. math::

   \mathbf{C} =
   \begin{pmatrix}
   1 & 0 & 1 \\
   0 & 1 & 1 \\
   0 & 0 & 1 \\
   \end{pmatrix}.

Go to A0.
