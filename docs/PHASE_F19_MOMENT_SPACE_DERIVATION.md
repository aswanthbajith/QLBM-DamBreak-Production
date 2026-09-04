# PHASE F19: MOMENT-SPACE DERIVATION FOR D2Q9 QLBM
## Orthogonal Moment Decomposition, Subspace Separation, and Hydrodynamic Invariants

---

## 1. D2Q9 Discrete Velocity Set
The D2Q9 lattice models 2D hydrodynamics using nine discrete velocity vectors $\mathbf{c}_i = (c_{ix}, c_{iy})$:
$$\mathbf{c}_0 = (0, 0)$$
$$\mathbf{c}_{1, 2, 3, 4} = (1, 0), (0, 1), (-1, 0), (0, -1)$$
$$\mathbf{c}_{5, 6, 7, 8} = (1, 1), (-1, 1), (-1, -1), (1, -1)$$
with standard lattice weights $w_0 = 4/9$, $w_{1..4} = 1/9$, $w_{5..8} = 1/36$, and speed of sound $c_s^2 = 1/3$.

---

## 2. Orthogonal Polynomial Transformation Matrix ($M$)
Using Gram-Schmidt orthogonalization of Hermite polynomials over discrete velocity space, the 9-dimensional population vector $\mathbf{f} = [f_0, f_1, \dots, f_8]^T$ maps to the orthogonal moment vector $\mathbf{m} = M \mathbf{f}$:

$$M = \begin{bmatrix}
 1 &  1 &  1 &  1 &  1 &  1 &  1 &  1 &  1 \\
-4 & -1 & -1 & -1 & -1 &  2 &  2 &  2 &  2 \\
 4 & -2 & -2 & -2 & -2 &  1 &  1 &  1 &  1 \\
 0 &  1 &  0 & -1 &  0 &  1 & -1 & -1 &  1 \\
 0 & -2 &  0 &  2 &  0 &  1 & -1 & -1 &  1 \\
 0 &  0 &  1 &  0 & -1 &  1 &  1 & -1 & -1 \\
 0 &  0 & -2 &  0 &  2 &  1 &  1 & -1 & -1 \\
 0 &  1 & -1 &  1 & -1 &  0 &  0 &  0 &  0 \\
 0 &  0 &  0 &  0 &  0 &  1 & -1 &  1 & -1
\end{bmatrix}$$

Because the rows of $M$ are mutually orthogonal with respect to the standard Euclidean inner product:
$$M M^T = \text{diag}(9, 36, 36, 6, 12, 6, 12, 4, 4)$$
the inverse mapping $\mathbf{f} = M^{-1} \mathbf{m}$ is exact and invertible.

---

## 3. Physical Identification of the 9 Modes

$$\begin{array}{|c|l|c|l|c|}
\hline
\textbf{Index } k & \textbf{Moment Symbol} & \textbf{Physical Definition} & \textbf{Subspace Sector} & \textbf{Relaxation Rate } s_k \\
\hline
0 & m_0 = \rho & \sum_i f_i & \mathbf{Conserved\ Mass} & s_0 = 0 \\
1 & m_1 = e & -4f_0 - \sum_{\text{axes}} f_i + 2\sum_{\text{diag}} f_i & \text{Non-Equilibrium Energy} & s_1 = \omega_f \\
2 & m_2 = \epsilon & 4f_0 - 2\sum_{\text{axes}} f_i + \sum_{\text{diag}} f_i & \text{Energy Squared} & s_2 = \omega_f \\
3 & m_3 = j_x & \sum_i f_i c_{ix} & \mathbf{Conserved\ X-Momentum} & s_3 = 0 \\
4 & m_4 = q_x & \text{Heat flux in } x & \text{Non-Equilibrium Flux} & s_4 = \omega_f \\
5 & m_5 = j_y & \sum_i f_i c_{iy} & \mathbf{Conserved\ Y-Momentum} & s_5 = 0 \\
6 & m_6 = q_y & \text{Heat flux in } y & \text{Non-Equilibrium Flux} & s_6 = \omega_f \\
7 & m_7 = p_{xx} & f_1 - f_2 + f_3 - f_4 & \text{Normal Stress Tensor} & s_7 = \omega_f \\
8 & m_8 = p_{xy} & f_5 - f_6 + f_7 - f_8 & \text{Shear Stress Tensor} & s_8 = \omega_f \\
\hline
\end{array}$$

---

## 4. Invariant Subspace Splitting & Collision Dynamics

In moment space, the general BGK/MRT collision decomposes diagonally:
$$\mathbf{m}^* = \mathbf{m} - S (\mathbf{m} - \mathbf{m}^{\text{eq}})$$
where $S = \text{diag}(0, \omega_f, \omega_f, 0, \omega_f, 0, \omega_f, \omega_f, \omega_f)$.

This establishes a fundamental direct-sum Hilbert space decomposition:
$$\boxed{\mathcal{H}_{\text{node}} = \mathcal{H}_{\text{cons}} \oplus \mathcal{H}_{\text{neq}}}$$
1. **Conserved Hydrodynamic Subspace** $\mathcal{H}_{\text{cons}} = \text{span}\{m_0, m_3, m_5\}$ (Dimension 3: $\rho, j_x, j_y$). In this subspace:
   $$\mathbf{m}_{\text{cons}}^* = \mathbf{m}_{\text{cons}} \quad (\text{Identity Operator: Strictly Reversible})$$
2. **Non-Equilibrium Dissipative Subspace** $\mathcal{H}_{\text{neq}} = \text{span}\{m_1, m_2, m_4, m_6, m_7, m_8\}$ (Dimension 6: $e, \epsilon, q_x, q_y, p_{xx}, p_{xy}$). In this subspace:
   $$\mathbf{m}_{\text{neq}}^* = (1 - \omega_f) \mathbf{m}_{\text{neq}} + \omega_f \mathbf{m}_{\text{neq}}^{\text{eq}} \quad (\text{Contractive Map: Strictly Non-Injective})$$

---

## 5. Equilibrium Moments
The equilibrium moments $\mathbf{m}^{\text{eq}}$ depend strictly on the conserved moments $(\rho, j_x, j_y)$:
$$\begin{aligned}
m_0^{\text{eq}} &= \rho \\
m_1^{\text{eq}} &= -2\rho + \frac{3}{\rho}(j_x^2 + j_y^2) \\
m_2^{\text{eq}} &= \rho - \frac{3}{\rho}(j_x^2 + j_y^2) \\
m_3^{\text{eq}} &= j_x \\
m_4^{\text{eq}} &= -j_x \\
m_5^{\text{eq}} &= j_y \\
m_6^{\text{eq}} &= -j_y \\
m_7^{\text{eq}} &= \frac{1}{\rho}(j_x^2 - j_y^2) \\
m_8^{\text{eq}} &= \frac{1}{\rho}(j_x j_y)
\end{aligned}$$
Because the non-equilibrium modes relax toward functions of conserved moments alone, any information present in the initial non-equilibrium components $\mathbf{m}_{\text{neq}}$ is systematically dissipated.
