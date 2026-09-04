# PHASE F20: DISSIPATIVE SUBSPACE & JACOBIAN ANALYSIS

## 1. Executive Summary
This document analyzes the spectral structure of the D2Q9 collision map in moment space to rigorously identify the dissipative degrees of freedom and distinguish them from the conserved hydrodynamic sector.

The analytical and numerical findings establish:
1. The collision Jacobian $J = \frac{\partial \mathbf{m}^*}{\partial \mathbf{m}}$ possesses exactly 3 invariant directions with eigenvalue $\lambda = 1.0$, corresponding to mass and momentum conservation $(\rho, j_x, j_y)$.
2. The collision Jacobian possesses exactly 6 contracting directions with eigenvalue $\lambda = 1.0 - \omega_f$, corresponding to the non-equilibrium modes $(e, \epsilon, q_x, q_y, p_{xx}, p_{xy})$.
3. When $\omega_f = 1.0$ (complete single-step relaxation), the 6 contracting eigenvalues collapse to $0.0$, creating an exact 6-dimensional kernel.

---

## 2. Jacobian Matrix Structure in Moment Space
In moment space, the diagonal relaxation collision operator without forcing is:
$$m_k^* = m_k - s_k (m_k - m_k^{\text{eq}}(\rho, j_x, j_y))$$
where the relaxation matrix is $S = \text{diag}(0, \omega_f, \omega_f, 0, \omega_f, 0, \omega_f, \omega_f, \omega_f)$.

Partitioning the moment vector into conserved modes $\mathbf{m}_{\text{cons}} = [\rho, j_x, j_y]^T \in \mathbb{R}^3$ and non-equilibrium modes $\mathbf{m}_{\text{neq}} = [e, \epsilon, q_x, q_y, p_{xx}, p_{xy}]^T \in \mathbb{R}^6$:
$$\mathbf{m}^* = \begin{bmatrix} \mathbf{m}_{\text{cons}}^* \\ \mathbf{m}_{\text{neq}}^* \end{bmatrix} = \begin{bmatrix} \mathbf{m}_{\text{cons}} \\ (1 - \omega_f)\mathbf{m}_{\text{neq}} + \omega_f \mathbf{m}_{\text{neq}}^{\text{eq}}(\mathbf{m}_{\text{cons}}) \end{bmatrix}$$

The Jacobian matrix $J = \frac{\partial \mathbf{m}^*}{\partial \mathbf{m}}$ has the exact block-triangular form:
$$J = \begin{bmatrix}
I_{3 \times 3} & 0_{3 \times 6} \\
\omega_f \frac{\partial \mathbf{m}_{\text{neq}}^{\text{eq}}}{\partial \mathbf{m}_{\text{cons}}} & (1 - \omega_f) I_{6 \times 6}
\end{bmatrix}$$

---

## 3. Eigenvalue Spectrum and Contracting Modes
Because $J$ is block-triangular, its eigenvalues are simply the union of the eigenvalues of the diagonal blocks:
$$\det(J - \lambda I_9) = \det(I_3 - \lambda I_3) \cdot \det((1 - \omega_f)I_6 - \lambda I_6) = (1 - \lambda)^3 \cdot (1 - \omega_f - \lambda)^6 = 0$$

### Spectral Decomposition:
1. **Conserved Invariant Eigenspace $\mathcal{E}_{\text{cons}}$** ($\lambda = 1.0$, multiplicity 3):
   Spanned by variations in density and momentum $(\delta \rho, \delta j_x, \delta j_y)$. These directions undergo zero contraction and zero dissipation.
2. **Dissipative Contracting Eigenspace $\mathcal{E}_{\text{neq}}$** ($\lambda = 1.0 - \omega_f$, multiplicity 6):
   Spanned by non-equilibrium perturbations $(\delta e, \delta \epsilon, \delta q_x, \delta q_y, \delta p_{xx}, \delta p_{xy})$.
   - For $0 < \omega_f < 2.0$, $|\lambda| < 1.0$ (strict contraction).
   - For $\omega_f = 1.0$, $\lambda = 0.0$ (complete projection onto the equilibrium manifold).

---

## 4. Singular Value Decomposition Across Relaxation Regimes
Numerical evaluation of the singular values of $J$ across physical relaxation times $\tau_f \in [0.5, 2.0]$ demonstrates:
- $\sigma_{\text{max}} \ge 1.0$ due to the off-diagonal equilibrium gradient coupling $\omega_f \frac{\partial \mathbf{m}_{\text{neq}}^{\text{eq}}}{\partial \mathbf{m}_{\text{cons}}}$.
- $\sigma_{\text{min}} = 1.0 - \omega_f$ along the pure non-equilibrium directions.
- For $\omega_f = 1.0$, the rank of the non-equilibrium block is 0, confirming that exactly 6 degrees of freedom are eliminated from the input state.

All numerical values are archived in [`results/phase_f20/dissipative_subspace.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/dissipative_subspace.csv).
