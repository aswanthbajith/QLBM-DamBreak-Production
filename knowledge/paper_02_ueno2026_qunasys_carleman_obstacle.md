# Knowledge Base Dossier: Ueno et al. (QunaSys & Univ of Tokyo, 2026)

## 1. Citation & Metadata
- **Title**: A Demonstration of Quantum Circuit Implementation for Obstacle Flow Using Carleman-Linearized Lattice Boltzmann Method
- **Authors**: Kazumasa Ueno (QunaSys & Dept of Earth and Planetary Science, Univ of Tokyo), Keita Kanno (QunaSys), Yasunori Lee (QunaSys)
- **Year**: May 27, 2026 (arXiv:2605.28135v1 [quant-ph])
- **Affiliations**: QunaSys (Bunkyo, Tokyo, Japan) & The University of Tokyo (Tokyo, Japan)
- **DOI / URL**: [arXiv:2605.28135](https://arxiv.org/abs/2605.28135)

---

## 2. Research Objective & Core Contribution
- **Objective**: Construct the first complete, gate-level quantum circuit implementation for 2D flow around an immersed solid obstacle with physical inflow, outflow, and no-slip bounce-back walls using Carleman-linearized LBM and QSVT-based matrix inversion.
- **Core Contribution**:
  - Implements non-periodic boundary conditions and obstacle geometry directly as sparse matrix operators embedded into quantum circuits via *index-value encoding*.
  - Solves the state amplitude exponential decay problem by introducing a *final state idling* mechanism in the grand linear system.
  - Formulates explicit block encodings for $A^{(1)}$ (one-step evolution) and $L$ (multi-time-step Carleman matrix).
  - Demonstrates logarithmic qubit and gate scaling with respect to spatial resolution $N$.

---

## 3. Physical Model & Governing PDEs
- **Continuum Equations**: Incompressible Navier-Stokes Equations:
  $$ \nabla \cdot \mathbf{u} = 0 $$
  $$ \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\frac{1}{\rho_0} \nabla p + \nu \nabla^2 \mathbf{u} $$
- **Weak Compressibility Approximation**:
  $$ \frac{1}{\rho} = (1 - (1 - \rho))^{-1} \approx 2 - \rho $$

---

## 4. Lattice Model & Discrete Velocity Set
- **Lattice**: D2Q9 (standard 2D 9-velocity).
- **Lattice vectors**: $\mathbf{c}_q \in \{ (0,0), (\pm 1, 0), (0, \pm 1), (\pm 1, \pm 1) \}$.
- **Weights**: $w_0 = 4/9$, $w_{1..4} = 1/9$, $w_{5..8} = 1/36$, $c_s^2 = 1/3$.

---

## 5. Equilibrium Distribution Function ($f_{q^*}^{eq}$)
- **Polynomial Expansion in Unshifted Distribution Functions $f$** (Eq. 2.17):
  $$ f_{q^*}^{eq}(\mathbf{x}_n, t) = w_{q^*} \sum_q f_q \left[ 1 + \frac{\mathbf{c}_q \cdot \mathbf{c}_{q^*}}{c_s^2} \right] + w_{q^*} \sum_{q, q'} f_q f_{q'} \left[ \frac{(\mathbf{c}_q \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q'} \cdot \mathbf{c}_{q^*})}{c_s^4} - \frac{\mathbf{c}_q \cdot \mathbf{c}_{q'}}{c_s^2} \right] + w_{q^*} \sum_{q, q', q''} f_q f_{q'} f_{q''} \left[ -\frac{(\mathbf{c}_q \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q'} \cdot \mathbf{c}_{q^*})}{2 c_s^4} + \frac{\mathbf{c}_q \cdot \mathbf{c}_{q'}}{2 c_s^2} \right] $$

---

## 6. Collision Operator & Tensor Matrices
- **Matrix-Vector Collision Equation** (Eq. 2.19):
  $$ \mathbf{f}^*(t) = (\mathbf{I} + \mathbf{F}_1) \mathbf{f}(t) + \mathbf{F}_2 \mathbf{f}^{\otimes 2}(t) + \mathbf{F}_3 \mathbf{f}^{\otimes 3}(t) $$
- **Tensor Matrix Elements** (Eq. 2.20):
  - Linear collision matrix $\mathbf{F}_1 \in \mathbb{R}^{NQ \times NQ}$:
    $$ (\mathbf{F}_1)_{(nQ + q^*)(nQ + q)} = \frac{1}{\tau} \left[ -\delta_{q^* q} + w_{q^*} \left( 1 + \frac{\mathbf{c}_q \cdot \mathbf{c}_{q^*}}{c_s^2} \right) \right] $$
  - Quadratic collision tensor $\mathbf{F}_2 \in \mathbb{R}^{NQ \times (NQ)^2}$:
    $$ (\mathbf{F}_2)_{(nQ + q^*)[(nQ + q)NQ + (nQ + q')]} = \frac{w_{q^*}}{\tau} \left[ \frac{(\mathbf{c}_q \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q'} \cdot \mathbf{c}_{q^*})}{c_s^4} - \frac{\mathbf{c}_q \cdot \mathbf{c}_{q'}}{c_s^2} \right] $$
  - Cubic collision tensor $\mathbf{F}_3 \in \mathbb{R}^{NQ \times (NQ)^3}$:
    $$ (\mathbf{F}_3)_{(nQ + q^*)[(nQ+q)(NQ)^2 + (nQ+q')NQ + (nQ+q'')]} = \frac{w_{q^*}}{\tau} \left[ -\frac{(\mathbf{c}_q \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q'} \cdot \mathbf{c}_{q^*})}{2 c_s^4} + \frac{\mathbf{c}_q \cdot \mathbf{c}_{q'}}{2 c_s^2} \right] $$

---

## 7. Streaming & Obstacle Boundary Condition Operators
- **Shift / Reflection Permutation Matrix $\mathbf{S}$** (Eq. 2.21, 2.22):
  $$ \mathbf{S}_{(n_{out} Q + q_{out})(n Q + q^*)} = 1 $$
  where destination node and direction are mapped by:
  - **Interior nodes**: $(\mathbf{x}_n + \mathbf{c}_{q^*}, q^*)$
  - **Obstacle & Wall bounce-back**: $(\mathbf{x}_n, \bar{q}^*)$ (reflection back into opposite lattice direction $\mathbf{c}_{\bar{q}^*} = -\mathbf{c}_{q^*}$)
  - **Inflow boundary**: $(\mathbf{x}_n, \bar{q}^*)$
  - **Outflow boundary**: $(\mathbf{x}_n + \mathbf{c}_{q^*} + \mathbf{c}_R, q^*)$

---

## 8. Multiphase Relevance
- The immersion of arbitrary 2D obstacles (dam structure, column, baffle) and wall boundaries via local reflection permutation operators provides the exact geometric operator required for dam-break obstacles.

---

## 9. Forcing Scheme
- Formulated as affine shift vector $\mathbf{h}_{force}$ added to the discrete update equation.

---

## 10. Carleman Linearization & Final State Idling
- **Carleman Truncation**: Tested primarily at order $N_C = 1$ (and extended formulation for $N_C \ge 2$).
- **Evolution Matrix with Boundary Conditions**:
  $$ \mathbf{f}(t+1) = \mathbf{A}^{(1)} \mathbf{f}(t) + \mathbf{h}_{bc} $$
  where $\mathbf{A}^{(1)} = \mathbf{S}(\mathbf{I} + \mathbf{F}_1) + \mathbf{B}_{in}$.
- **Final State Idling Technique**:
  Appends identity transitions for $t > T_{sim}$ up to total dimension $T_{idling}$, eliminating exponential decay of quantum amplitudes during multi-step measurement.

---

## 11. Quantum Circuit Architecture & Block Encodings
- **Index-Value Encoding**: Embeds sparse matrix non-zero indices and values into quantum oracles $O_F, O_A$.
- **Block-Encoding of $A^{(1)}$** (Eq. 2.39):
  $$ U_{A^{(1)}} = (\langle 0|^{\otimes a} \otimes \mathbf{I}) U_{A^{(1)}} (|0\rangle^{\otimes a} \otimes \mathbf{I}) = \frac{\mathbf{A}^{(1)}}{\alpha_A} $$
  Subnormalization factor: $\alpha_A = \|\mathbf{A}^{(1)}\|_{\max} \cdot s_{sparse}$.
- **Block-Encoding of Grand System $L$**:
  Constructed from $U_{A^{(1)}}$ and shift registers using QSVT.

---

## 12. Validation & Numerical Benchmarks
- 2D flow around a square obstacle ($Re = 1.0, Ma = 0.01$).
- Comparison between:
  1. Classical LBM simulation.
  2. Quantum circuit simulation (statevector / shot-based).
  3. Classical polynomial emulation via the Clenshaw recurrence algorithm.

---

## 13. Quantum Computational Costs & Scaling
- **Qubit Count**: $n_{qubits} = \mathcal{O}(\log_2 N + \log_2 Q + \log_2 T)$.
- **Gate Complexity**: $\mathcal{O}(\text{polylog}(N) \cdot T \cdot \kappa(L))$.
- **Fault-Tolerant T-Gate Cost**: Explicitly evaluated using state-of-the-art Q-REAP / surface code synthesizers.

---

## 14. Linear vs. Nonlinear Term Catalog
| Term | Form | Mathematical Type | Quantum Implementation |
| :--- | :--- | :--- | :--- |
| First-order LBE | $\mathbf{A}^{(1)} = \mathbf{S}(\mathbf{I} + \mathbf{F}_1)$ | Linear Operator | Block encoding via index-value oracle |
| Obstacle Bounce-Back | $\mathbf{S}_{obs}: (n, q^*) \mapsto (n, \bar{q}^*)$ | Permutation | Swap gates on velocity register |
| Quadratic Nonlinearity | $\mathbf{F}_2 \mathbf{f}^{\otimes 2}$ | Degree-2 Tensor | $N_C=2$ Carleman block |
| Cubic Nonlinearity | $\mathbf{F}_3 \mathbf{f}^{\otimes 3}$ | Degree-3 Tensor | $N_C=3$ Carleman block |
| Boundary Affine Term | $\mathbf{h}_{bc}$ | Constant Vector | State preparation oracle $U_b$ |

---

## 15. Key Takeaways for Dam-Break QLBM
1. **Obstacle Representation**: Solid walls and obstacles in dam breaks do not require complex potential fields—they are implemented as exact permutation swap gates $\mathbf{c}_q \leftrightarrow -\mathbf{c}_q$ on boundary nodes.
2. **Matrix Sparsity**: The full evolution matrix has $\mathcal{O}(Q)$ sparsity per row regardless of grid size $N$, making block encoding highly efficient ($\alpha = \mathcal{O}(1)$).
