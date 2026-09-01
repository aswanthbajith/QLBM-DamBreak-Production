# FINAL QUANTUM ARCHITECTURE: TWO-PHASE D2Q9 DAM-BREAK QLBM

**Architecture Specification**: End-to-End Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Target Physical System**: 2D Two-Phase Dam-Break Column Collapse in an Enclosed Box (D2Q9 Lattice)  
**Implementation Snapshot**: `/home/aswa/Research/QLBM-DamBreak-Production`  

---

## 1. Authoritative Physical Model

The physical system models the transient collapse of a rectangular column of dense liquid ($\rho_L = 1.0$) surrounded by light gas ($\rho_G = 0.1$) under gravitational acceleration $g_{\text{acc}} = -0.001$ inside a closed solid rectangular cavity of size $N_x \times N_y$.

* **Hydrodynamic Kinetic Distribution**: $f_i(\mathbf{x}, t) \in \mathbb{R}^9$ ($i = 0, \ldots, 8$).
* **Order-Parameter Distribution**: $g_i(\mathbf{x}, t) \in \mathbb{R}^9$ ($i = 0, \ldots, 8$).
* **Macroscopic Fields**:
  $$\rho(\mathbf{x}, t) = \sum_{i=0}^8 f_i(\mathbf{x}, t), \quad \mathbf{u}(\mathbf{x}, t) = \frac{1}{\rho(\mathbf{x}, t)} \sum_{i=0}^8 \mathbf{c}_i f_i(\mathbf{x}, t), \quad \phi(\mathbf{x}, t) = \sum_{i=0}^8 g_i(\mathbf{x}, t)$$
* **Collision Relaxations (BGK)**:
  $$f_i^* = f_i - \frac{1}{\tau_f} (f_i - f_i^{\text{eq}}(\rho, \mathbf{u})) + \Delta f_i^{\text{force}}$$
  $$g_i^* = g_i - \frac{1}{\tau_g} (g_i - g_i^{\text{eq}}(\phi, \mathbf{u}))$$

---

## 2. Quantum State & Register Architecture

### A. Hilbert Space Representation
The fluid state on an $N_x \times N_y$ lattice is represented in a 9-qubit Hilbert space $\mathcal{H}_{512} = (\mathbb{C}^2)^{\otimes 9}$ ($\dim \mathcal{H} = 512$):

$$|\Psi(t)\rangle = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 \left[ \sqrt{\frac{f_i(x,y,t)}{M}} |x, y, i, s=0\rangle + \sqrt{\frac{g_i(x,y,t)}{M}} |x, y, i, s=1\rangle \right]$$

where $M = \sum_{x,y,i} [f_i(x,y,t) + g_i(x,y,t)]$ is the global mass scalar.

### B. Register Allocation ($4 \times 4$ Lattice)
| Register Name | Qubits | Bit Indices | Physical Meaning |
| :--- | :---: | :---: | :--- |
| `pos_x` | $n_{qx} = 2$ | $q_0, q_1$ | Spatial $x$-coordinate ($x \in \{0, 1, 2, 3\}$) |
| `pos_y` | $n_{qy} = 2$ | $q_2, q_3$ | Spatial $y$-coordinate ($y \in \{0, 1, 2, 3\}$) |
| `velocity` | $n_{qvel} = 4$ | $q_4, q_5, q_6, q_7$ | D2Q9 velocities $i \in \{0..8\}$ ($9..15$ are padding states) |
| `selector` | $n_{qsel} = 1$ | $q_8$ | Distribution selector: $s=0 \to f_i$, $s=1 \to g_i$ |
| `ancilla` | $n_{\text{anc}} = 1$ | $q_9$ | Sz.-Nagy block-encoding postselection ancilla |

---

## 3. Quantum Timestep Operators

The unified timestep operator evolves the system through 4 distinct stages:

$$|\Psi_{t+1}\rangle = B \cdot S \cdot U_{\text{force}} \cdot U_{\text{collision}} |\Psi_t\rangle$$

```text
    |Ψ_t⟩
      │
      ▼
┌──────────────┐
│ U_collision  │  10-Qubit Sz.-Nagy Unitary Dilation of Local Carleman Map A_eval
└──────┬───────┘
      │
      ▼
┌──────────────┐
│   U_force    │  Block-encoded gravitational buoyancy perturbation
└──────┬───────┘
      │
      ▼
┌──────────────┐
│      S       │  Reversible 512-dim spatial coordinate shift permutation (S† S = I)
└──────┬───────┘
      │
      ▼
┌──────────────┐
│      B       │  Direction-selective wall bounce-back involution (B² = I, B† B = I)
└──────┬───────┘
      │
      ▼
   |Ψ_{t+1}⟩
```

### A. Local Carleman Collision ($U_{\text{collision}}$)
* **Local State**: $\Psi_{\text{node}} = [f_0..f_8, g_0..g_8]^T \in \mathbb{R}^{18}$.
* **Polynomial Lift**: $\mathbf{Y}_2 = [\Psi; \Psi \otimes \Psi] \in \mathbb{R}^{342}$.
* **Step Evaluation Operator**: $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$.
* **Sz.-Nagy Unitary Dilation**:
  $$U_C = \begin{pmatrix} \bar{A} & \sqrt{I - \bar{A}\bar{A}^\dagger} \\ \sqrt{I - \bar{A}^\dagger\bar{A}} & -\bar{A}^\dagger \end{pmatrix} \in \mathbb{U}(1024 = 2^{10})$$
  where $\bar{A} = \widetilde{A}_{\text{padded}} / \alpha$ with $\alpha = 1.01 \|\widetilde{A}\|_2 \approx 58.75$.
* **Unitarity**: Machine-precision unitary: $\|U_C^\dagger U_C - I_{1024}\|_2 < 10^{-13}$.

### B. Quantum Buoyancy Forcing ($U_{\text{force}}$)
* **Buoyancy Increment**: $\Delta f_i = 3 w_i (\rho - \rho_G) g_{\text{acc}} c_{iy}$.
* **Unitary Dilation**: $U_{\text{force}} \in \mathbb{U}(1024)$ applying diagonal affine velocity scaling conditioned on $s=0$.

### C. Reversible Spatial Streaming ($S$)
* **Permutation Mapping**:
  $$S |x, y, v, s\rangle = |(x + c_{vx}) \bmod N_x, (y + c_{vy}) \bmod N_y, v, s\rangle \quad (\forall v \in \{0..8\})$$
  $$S |x, y, v, s\rangle = |x, y, v, s\rangle \quad (\forall v \ge 9)$$
* **Unitarity**: Machine precision: $\|S^\dagger S - I_{512}\|_2 = 0.000000$.

### D. Boundary Bounce-Back Involution ($B$)
* **Wall-Hitting Reflection**:
  $$B |x_b, y_b, v, s\rangle = |x_b, y_b, \text{OPPOSITE}[v], s\rangle \quad (\text{if } \mathbf{c}_v \cdot \mathbf{n}_{\text{wall}} > 0)$$
  $$B |x, y, v, s\rangle = |x, y, v, s\rangle \quad (\text{interior, tangential, and padding states})$$
* **Involution Property**:
  $$B = B^\dagger, \quad B^2 = I_{512}, \quad \|B^\dagger B - I_{512}\|_2 = 0.000000$$

---

## 4. Macroscopic Observable Estimation

Macroscopic fields are extracted via expectation values without intermediate array destruction:
* **Density Field**: $\rho(x, y) = M \langle \Psi | \hat{\Pi}_\rho(x, y) | \Psi \rangle$
* **Phase Field**: $\phi(x, y) = M \langle \Psi | \hat{\Pi}_\phi(x, y) | \Psi \rangle$
* **Velocity Field**: $u_x(x, y) = \frac{M}{\rho(x, y)} \langle \Psi | \hat{C}_x(x, y) | \Psi \rangle, \quad u_y(x, y) = \frac{M}{\rho(x, y)} \langle \Psi | \hat{C}_y(x, y) | \Psi \rangle$

---

## 5. Architectural Complexity & Scaling

* **Qubit Requirement**: $n = \lceil\log_2 N_x\rceil + \lceil\log_2 N_y\rceil + 4 + 1 + 1 = O(\log N)$ qubits.
* **Spatial Circuit Depth**: $O(\text{poly}(\log N))$ gates for streaming and boundary reflections.
* **Postselection Probability**: $P_{\text{succ}} \approx \alpha^{-2} \sim 10^{-3} - 10^{-4}$ per block-encoded collision step.
