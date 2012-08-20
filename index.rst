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

1. If :math:`A>B - \varepsilon` or
(:math:`\overline{|A-B|>\varepsilon}` and :math:`|\xi|>|\eta| - \varepsilon`),

   .. math::

      \mathbf{C} =
      \begin{pmatrix}
      0 & -1 & 0 \\
      -1 & 0 & 0 \\
      0 & 0 & -1 \\
      \end{pmatrix}.

2. If :math:`B>C-\varepsilon` or (:math:`\overline{|B-C|>\varepsilon}`
and :math:`|\eta|>|\zeta| - \varepsilon`),

   .. math::

      \mathbf{C} =
      \begin{pmatrix}
      -1 & 0 & 0 \\
      0 & 0 & -1 \\
      0 & -1 & 0 \\
      \end{pmatrix}.

3. If :math:`\xi\eta\zeta > -\varepsilon`:

   :math:`i=-1` if :math:`\xi<-\varepsilon` else :math:`i=1`,
   :math:`j=-1` if :math:`\eta<-\varepsilon` else :math:`j=1`, and
   :math:`k=-1` if :math:`\zeta<-\varepsilon` else :math:`k=1` for

   .. math::

      \mathbf{C} =
      \begin{pmatrix}
      i & 0 & 0 \\
      0 & j & 0 \\
      0 & 0 & k \\
      \end{pmatrix}.

4. If :math:`\overline{\xi\eta\zeta > \varepsilon}`:

   :math:`i=-1` if :math:`\xi<0` else :math:`i=1`,
   :math:`j=-1` if :math:`\eta<0` else :math:`j=1`, and
   :math:`k=-1` if :math:`\zeta<0` else :math:`k=1` for
