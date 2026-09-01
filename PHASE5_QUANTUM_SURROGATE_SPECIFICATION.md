# PHASE 5 QUANTUM-SUITABLE SURROGATE MODEL SPECIFICATION

**Status**: Official Specification for Phase 5 Quantum Pipeline  
**Model Name**: Constant-Density Quadratic Two-Phase LBM Surrogate (CDQ-QLBM)  
**Author**: Lead Scientific Software Architect & Quantum Algorithms Engineer  

---

## 1. Mathematical & Physical Foundations

### 1.1 Physical Domain and Grid
* **Domain**: 2D Cartesian lattice $\Omega = [0, L_x] \times [0, L_y]$ discretized uniformly with $N = N_x \times N_y$ lattice nodes.
* **Lattice Velocity Set**: Standard two-dimensional nine-velocity (D2Q9) model:
  $$\mathbf{c}_0 = (0, 0)$$
  $$\mathbf{c}_{1,2,3,4} = (\pm 1, 0), (0, \pm 1)$$
  $$\mathbf{c}_{5,6,7,8} = (\pm 1, \pm 1)$$
* **Lattice Weights**: $w_0 = 4/9$, $w_{1..4} = 1/9$, $w_{5..8} = 1/36$.
* **Speed of Sound**: $c_s^2 = 1/3$, $c_s^4 = 1/9$.

### 1.2 Physical State Variables
* **Hydrodynamic Distribution**: $g_q(\mathbf{x}, t) \in \mathbb{R}$ for $q \in \{0, \dots, 8\}$.
  * Density: $\rho(\mathbf{x}, t) = \sum_{q=0}^8 g_q(\mathbf{x}, t) \approx \rho_0 = 1.0$.
  * Velocity: $\mathbf{u}(\mathbf{x}, t) = \frac{1}{\rho_0} \sum_{q=0}^8 g_q(\mathbf{x}, t) \mathbf{c}_q$.
* **Phase-Field Distribution**: $h_q(\mathbf{x}, t) \in \mathbb{R}$ for $q \in \{0, \dots, 8\}$.
  * Order Parameter: $\phi(\mathbf{x}, t) = \sum_{q=0}^8 h_q(\mathbf{x}, t) \in [0, 1]$ ($0 = \text{gas}, 1 = \text{liquid}$).

---

## 2. Collision and Polynomial Formulations

### 2.1 Assumptions for Exact Quadratic ($p=2$) Closure
1. **Constant Reference Density**: $\rho \approx \rho_0$ in momentum denominators (incompressible approximation).
2. **Constant Viscosity & Mobility**: Relaxation times $\tau_v$ and $\tau_\phi$ are spatially homogeneous.
3. **Linearized Advective Fluxes**:
   * Hydrodynamic equilibrium:
     $$g_q^{\text{eq}} = w_q \left[ \rho_0 + \frac{\mathbf{c}_q \cdot (\rho_0 \mathbf{u})}{c_s^2} + \frac{(\mathbf{c}_q \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]$$
   * Phase-field equilibrium:
     $$h_q^{\text{eq}} = w_q \phi \left[ 1 + \frac{\mathbf{c}_q \cdot \mathbf{u}}{c_s^2} \right]$$

### 2.2 Algebraic Polynomial Degree
The state update before streaming decomposes into linear and quadratic monomial operators:
$$\mathbf{g}^*(\mathbf{x}) = M_1^g \mathbf{g}(\mathbf{x}) + M_2^g [\mathbf{g}(\mathbf{x}) \otimes \mathbf{g}(\mathbf{x})]$$
$$\mathbf{h}^*(\mathbf{x}) = M_1^h \mathbf{h}(\mathbf{x}) + M_2^h [\mathbf{h}(\mathbf{x}) \otimes \mathbf{g}(\mathbf{x})]$$
The polynomial degree is strictly **$p = 2$**.

---

## 3. Quantum State Space & Carleman Linearization

### 3.1 Base and Lifted State Vectors
* **Base State**: $\Psi(t) = [\mathbf{g}(t); \mathbf{h}(t)] \in \mathbb{R}^{18 N}$.
* **Local Quadratic Lifting**: For each node $n$, compute local Kronecker product $\Psi_n^{\otimes 2} = \Psi_n \otimes \Psi_n \in \mathbb{R}^{324}$.
* **Carleman State Vector**:
  $$Y(t) = \begin{bmatrix} \Psi(t) \\ \Psi_{\text{local}}^{\otimes 2}(t) \end{bmatrix} \in \mathbb{R}^{342 N}$$

### 3.2 Full Carleman Linear Matrix $A_C$
$$A_C = S_C \cdot C_2 \in \mathbb{R}^{342 N \times 342 N}$$
where:
* $C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1^{\otimes 2} \end{bmatrix}$ is the block upper-triangular collision matrix.
* $S_C = \text{diag}(S_{\text{base}}, S_{\text{kron2}})$ is the unitary streaming permutation matrix.

---

## 4. Quantum Algorithmic Execution

### 4.1 Unitary Block Encoding
Canonical CS/Halmos dilation $U_A \in \mathbb{C}^{2d \times 2d}$ ($d = 2^{\lceil \log_2(342 N) \rceil}$):
$$U_A = \begin{bmatrix} A_C / \alpha & \sqrt{I - (A_C / \alpha)(A_C / \alpha)^\dagger} \\ \sqrt{I - (A_C / \alpha)^\dagger (A_C / \alpha)} & -(A_C / \alpha)^\dagger \end{bmatrix}$$
with subnormalization constant $\alpha = 11.4739$.

### 4.2 QSVT Inversion Operator
Solves linear step $(I + \Delta t A_C) Y(t+1) = Y(t)$ using degree $d=15$ odd Chebyshev polynomial $P(x) \approx 1/(\alpha x)$ bounded by $|P(x)| \le 0.95$.

### 4.3 Observable Extraction
* **Surge Front $x^*$**: $x^* = \max \{ x \mid \phi(x, y_{\text{floor}}) > 0.5 \} / H_{\text{dam}}$.
* **Column Height $h^*$**: $h^* = \max \{ y \mid \phi(x_{\text{wall}}, y) > 0.5 \} / H_{\text{dam}}$.
* **Total Mass $M$**: $M = \sum_{\mathbf{x}} \phi(\mathbf{x})$.

---

## 5. Scope Boundaries and Limitations
1. This model is a **quantum-suitable mathematical surrogate**, not an exact quantum solver for high-density-ratio (1000:1) variable-density water-air Navier-Stokes equations.
2. Full physical validation is referenced against the classical ground truth solver (`classical/two_phase_lbm.py`).
