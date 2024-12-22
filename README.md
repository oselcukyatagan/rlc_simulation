# rlc_simulation


The over-damped response logic may seem complicated at first glance, so it may be useful to explain.

We know that the over-damped condition response will be in the form of

\[x(t) = A_1 e^{s_1t} + A_2 e^{s_2t} \quad (5)\]

Calculating s_1​ and s_2​ is fairly straightforward. To calculate A_1​ and A_2, the equations in Figure 1 must be solved simultaneously.

![over-damp logic](https://github.com/user-attachments/assets/2cb080f3-b0ec-43fe-bcc0-8e63970c5509)
*Figure 1: over-damp logic.*
Nilsson, J. W., & Riedel, S. A. (2014). Electric circuits (10th ed.). Pearson.

These equations can be expressed in matrix form as, 

\[
\begin{bmatrix}
1 & 1 \\
s1 & s2
\end{bmatrix}
\begin{bmatrix}
V_c \\
\frac{dV_c}{dt}
\end{bmatrix}
=
\begin{bmatrix}
A1 \\
1
\end{bmatrix}
\]

Which I implemented and solved as seen in Figure 2 below.

![over-damp code](https://github.com/user-attachments/assets/dbac41fc-d2e1-4612-b5f5-31254f56b664)
*Figure 2: over-damp logic python code.*
