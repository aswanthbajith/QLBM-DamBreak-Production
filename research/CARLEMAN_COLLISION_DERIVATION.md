# MATHEMATICAL DERIVATION: LOCAL CARLEMAN LINEARIZATION FOR TWO-PHASE D2Q9 LATTICE BOLTZMANN COLLISION

**Date**: 2026-08-25  
**Author**: Lead Quantum CFD Algorithm Engineer  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Classical D2Q9 Kinetic Equations

For each lattice node $\mathbf{x} = (x, y)$, the two-phase D2Q9 system is governed by two sets of 9 discrete velocity populations:
1. **Hydrodynamic populations** $f_i(\mathbf{x}, t)$ ($i=0, \dots, 8$) describing mass density $\rho$ and momentum density $\mathbf{j} = \rho \mathbf{u}$.
2. **Order-parameter populations** $g_i(\mathbf{x}, t)$ ($i=0, \dots, 8$) describing the phase field $\phi \in [0, 1]$.

### Discrete Velocities and Lattice Weights
The 9 discrete velocity vectors $\mathbf{c}_i = (c_{ix}, c_{iy})^T$ and lattice weights $w_i$ are:
$$\mathbf{c}_0 = (0, 0), \quad w_0 = \frac{4}{9}$$
$$\mathbf{c}_{1..4} = (\pm 1, 0), (0, \pm 1), \quad w_{1..4} = \frac{1}{9}$$
$$\mathbf{c}_{5..8} = (\pm 1, \pm 1), \quad w_{5..8} = \frac{1}{36}$$
with speed of sound $c_s^2 = 1/3$ and $c_s^4 = 1/9$.

---

## 2. Macroscopic Moments and Equilibria

The local macroscopic moments are:
$$\rho = \sum_{i=0}^8 f_i, \quad j_x = \rho u_x = \sum_{i=0}^8 c_{ix} f_i, \quad j_y = \rho u_y = \sum_{i=0}^8 c_{iy} f_i, \quad \phi = \sum_{i=0}^8 g_i$$

### Exact BGK Relaxation Map
The post-collision distributions $f_i^*$ and $g_i^*$ are:
$$f_i^* = (1 - \omega_f) f_i + \omega_f f_i^{\text{eq}}(\rho, \mathbf{u})$$
$$g_i^* = (1 - \omega_g) g_i + \omega_g g_i^{\text{eq}}(\phi, \mathbf{u})$$
where $\omega_f = 1/\tau_f$ and $\omega_g = 1/\tau_g$.

The continuous equilibrium expansions are:
$$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]$$
$$g_i^{\text{eq}}(\phi, \mathbf{u}) = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right]$$

---

## 3. Polynomial Structure of the Collision Operator

Substituting $\mathbf{u} = \mathbf{j}/\rho$ into $f_i^{\text{eq}}$ and $g_i^{\text{eq}}$:
$$f_i^{\text{eq}} = w_i \left[ \rho + 3 (\mathbf{c}_i \cdot \mathbf{j}) + \frac{9}{2} \frac{(\mathbf{c}_i \cdot \mathbf{j})^2}{\rho} - \frac{3}{2} \frac{|\mathbf{j}|^2}{\rho} \right]$$
$$g_i^{\text{eq}} = w_i \left[ \phi + 3 \frac{\phi (\mathbf{c}_i \cdot \mathbf{j})}{\rho} \right]$$

Notice the decomposition into linear and nonlinear terms:
1. **Linear Terms**:
   * $\rho = \sum_{j=0}^8 f_j = \mathbf{1}^T f$
   * $\mathbf{c}_i \cdot \mathbf{j} = \sum_{j=0}^8 (\mathbf{c}_i \cdot \mathbf{c}_j) f_j$
   * $\phi = \sum_{j=0}^8 g_j = \mathbf{1}^T g$
2. **Quadratic Rational Terms**:
   * $\mathcal{Q}_i(f) = \frac{w_i}{\rho} \left[ \frac{9}{2} (\mathbf{c}_i \cdot \mathbf{j})^2 - \frac{3}{2} |\mathbf{j}|^2 \right]$
   * $\mathcal{A}_i(f, g) = \frac{3 w_i}{\rho} \phi (\mathbf{c}_i \cdot \mathbf{j})$

### Resolution of the Rational $1/\rho$ Factor (Route A vs Route B)

* **Route A (Reference Density Normalization)**:
  In standard low-Mach lattice Boltzmann hydrodynamics ($|\delta\rho/\rho_0| \ll 1$), the quadratic convective fluxes are evaluated with respect to the phase reference density $\rho_0$ ($\rho_{\text{liquid}}$ or $\rho_{\text{gas}}$):
  $$\frac{1}{\rho} = \frac{1}{\rho_0} + \mathcal{O}(\text{Ma}^2 \delta\rho)$$
  This truncates the rational dependence into a strictly quadratic polynomial:
  $$\mathcal{Q}_i(f) = \frac{w_i}{\rho_0} \sum_{k=0}^8 \sum_{l=0}^8 \left[ \frac{9}{2} (\mathbf{c}_i \cdot \mathbf{c}_k)(\mathbf{c}_i \cdot \mathbf{c}_l) - \frac{3}{2} (\mathbf{c}_k \cdot \mathbf{c}_l) \right] f_k f_l$$
  $$\mathcal{A}_i(f, g) = \frac{3 w_i}{\rho_0} \sum_{k=0}^8 \sum_{l=0}^8 (\mathbf{c}_i \cdot \mathbf{c}_k) g_l f_k$$
  This choice is exact for incompressible two-phase flows and is adopted here.

---

## 4. Local Carleman Lifting Formulation

Let the local state vector at node $\mathbf{x}$ be:
$$\Psi = \begin{pmatrix} f \\ g \end{pmatrix} \in \mathbb{R}^{18}$$

The dynamical equation for $\Psi$ during collision is:
$$\Psi^* = M_1 \Psi + M_2 (\Psi \otimes \Psi)$$
where:
* $M_1 \in \mathbb{R}^{18 \times 18}$ is the linear collision matrix.
* $M_2 \in \mathbb{R}^{18 \times 324}$ is the quadratic contraction tensor mapping $\Psi^{\otimes 2} \in \mathbb{R}^{324}$ into $\mathbb{R}^{18}$.

### Second-Order Carleman Lifted State
We enlarge the state vector to the Carleman state:
$$Y_2 = \begin{pmatrix} \Psi \\ \Psi \otimes \Psi \end{pmatrix} \in \mathbb{R}^{18 + 324} = \mathbb{R}^{342}$$

The evolution of the quadratic Kronecker product $\Psi^{\otimes 2}$ under linear truncation is:
$$(\Psi^*)^{\otimes 2} = (M_1 \Psi + M_2 \Psi^{\otimes 2}) \otimes (M_1 \Psi + M_2 \Psi^{\otimes 2}) = (M_1 \otimes M_1) \Psi^{\otimes 2} + \mathcal{O}(\Psi^{\otimes 3})$$

Truncating at order $N_C = 2$, the nonlinear collision is transformed into the **exact linear system**:
$$Y_2^* = C_2 Y_2$$
where $C_2 \in \mathbb{R}^{342 \times 342}$ is the block upper-triangular Carleman collision matrix:
$$C_2 = \begin{pmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{pmatrix}$$

### Dimension Count

| Variable Layer | Single-Phase Dimension | Two-Phase Coupled Dimension |
| :--- | :--- | :--- |
| **Linear Base $\Psi$** | $9$ ($f_0 \dots f_8$) | $18$ ($f_0 \dots f_8, g_0 \dots g_8$) |
| **Quadratic Monomials $\Psi^{\otimes 2}$** | $9 \times 9 = 81$ | $18 \times 18 = 324$ |
| **Total Carleman State $Y_2$** | **$90$** | **$342$** |

---

## 5. Non-Unitary Dissipation & Unitary Dilation / Block Encoding

Because $C_2$ represents dissipative kinetic relaxation, $\|C_2\|_2 \neq 1$.
To execute $C_2$ on a quantum computer without violating unitarity:
1. Compute the operator spectral norm: $\alpha \ge \|C_2\|_2$.
2. Define the contractive normalized matrix:
   $$\bar{C}_2 = \frac{C_2}{\alpha}, \quad \|\bar{C}_2\|_2 \le 1$$
3. Construct the **Unitary Dilation** (Block Encoding) $U_{C} \in U(2 \times 342)$:
   $$U_{C} = \begin{pmatrix} \bar{C}_2 & \sqrt{I - \bar{C}_2 \bar{C}_2^\dagger} \\ \sqrt{I - \bar{C}_2^\dagger \bar{C}_2} & -\bar{C}_2^\dagger \end{pmatrix}$$
   which strictly satisfies:
   $$U_C^\dagger U_C = I_{684}$$
4. **Ancilla Projective Extraction**:
   Preparing $|0\rangle_{\text{anc}} |Y_2\rangle$ and applying $U_C$:
   $$U_C (|0\rangle |Y_2\rangle) = |0\rangle (\bar{C}_2 |Y_2\rangle) + |1\rangle (\sqrt{I - \bar{C}_2^\dagger \bar{C}_2} |Y_2\rangle)$$
   Projecting onto ancilla state $|0\rangle$ yields the exact post-collision Carleman state $\frac{1}{\alpha} C_2 |Y_2\rangle$ with success probability:
   $$P_{\text{success}} = \|\bar{C}_2 |Y_2\rangle\|^2 = \frac{\|C_2 |Y_2\rangle\|^2}{\alpha^2}$$
