# PHASE F20: D2Q9 MOMENT-SPACE DERIVATION & ORTHOGONALITY PROOF

## 1. Gram-Schmidt / Hermite Moment Basis
In the D2Q9 lattice velocity space, the 9 discrete populations $\mathbf{f} = [f_0, f_1, \dots, f_8]^T$ are transformed to orthogonal polynomial moments $\mathbf{m} = [m_0, m_1, \dots, m_8]^T$ via the transformation matrix $M \in \mathbb{R}^{9 \times 9}$:
$$\mathbf{m} = M \mathbf{f}, \qquad \mathbf{f} = M^{-1} \mathbf{m}$$

The explicit orthogonal Hermite transformation matrix is:
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

---

## 2. Moment Indexing and Physical Meaning

| Index $k$ | Symbol | Physical Meaning | Sector | Conserved? | Relaxation Rate $s_k$ |
| :---: | :---: | :--- | :---: | :---: | :---: |
| $0$ | $\rho$ | Fluid Density (Mass) | $\mathcal{H}_{\text{cons}}$ | **YES** | $0.0$ |
| $1$ | $e$ | Kinetic Energy Mode | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |
| $2$ | $\epsilon$ | Energy Squared Mode | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |
| $3$ | $j_x$ | Momentum Density in $x$ | $\mathcal{H}_{\text{cons}}$ | **YES** | $0.0$ |
| $4$ | $q_x$ | Heat Flux in $x$ | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |
| $5$ | $j_y$ | Momentum Density in $y$ | $\mathcal{H}_{\text{cons}}$ | **YES** | $0.0$ |
| $6$ | $q_y$ | Heat Flux in $y$ | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |
| $7$ | $p_{xx}$ | Normal Stress $(f_1 - f_2 + f_3 - f_4)$ | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |
| $8$ | $p_{xy}$ | Shear Stress $(f_5 - f_6 + f_7 - f_8)$ | $\mathcal{H}_{\text{neq}}$ | NO | $\omega_f$ |

---

## 3. Orthogonality and Inversion Proof
The row vectors $\mathbf{v}_i$ of $M$ are mutually orthogonal:
$$\langle \mathbf{v}_i, \mathbf{v}_j \rangle = \mathbf{v}_i \mathbf{v}_j^T = 0 \quad \forall i \neq j$$

The diagonal Gramian matrix is:
$$M M^T = \text{diag}(9, 36, 36, 6, 12, 6, 12, 4, 4)$$

Hence, the exact matrix inverse is computed analytically as:
$$M^{-1} = M^T (M M^T)^{-1}$$
which yields machine-precision reconstruction:
$$\|M^{-1} M - I\|_2 < 10^{-15}, \qquad \|M M^{-1} - I\|_2 < 10^{-15}$$
as recorded in [`results/phase_f20/moment_transform.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/moment_transform.csv).

---

## 4. Equilibrium Moments
The equilibrium moments $\mathbf{m}^{\text{eq}}$ depend solely on the conserved hydrodynamic variables $(\rho, j_x, j_y)$:
$$m_0^{\text{eq}} = \rho$$
$$m_1^{\text{eq}} = -2\rho + \frac{3}{\rho}(j_x^2 + j_y^2)$$
$$m_2^{\text{eq}} = \rho - \frac{3}{\rho}(j_x^2 + j_y^2)$$
$$m_3^{\text{eq}} = j_x$$
$$m_4^{\text{eq}} = -j_x$$
$$m_5^{\text{eq}} = j_y$$
$$m_6^{\text{eq}} = -j_y$$
$$m_7^{\text{eq}} = \frac{1}{\rho}(j_x^2 - j_y^2)$$
$$m_8^{\text{eq}} = \frac{1}{\rho} j_x j_y$$

Notice that for all non-equilibrium moments $k \in \{1, 2, 4, 6, 7, 8\}$, $m_k^{\text{eq}}$ is a nonlinear algebraic function of $\rho, j_x, j_y$.
In local equilibrium ($\mathbf{m} = \mathbf{m}^{\text{eq}}$), the non-equilibrium deviation is identically zero:
$$\Delta \mathbf{m}_{\text{neq}} = \mathbf{m}_{\text{neq}} - \mathbf{m}_{\text{neq}}^{\text{eq}} = \mathbf{0}$$
This algebraic structure is what enables the environment coupling to be confined strictly to $\mathcal{H}_{\text{neq}}$.
