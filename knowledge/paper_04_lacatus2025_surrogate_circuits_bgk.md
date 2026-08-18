# Knowledge Base Dossier: Lăcătuș & Möller (TU Delft, 2025)

## 1. Citation & Metadata
- **Title**: Surrogate Quantum Circuit Design for the Lattice Boltzmann Collision Operator
- **Authors**: Monica Lăcătuș, Matthias Möller
- **Year**: Nov 13, 2025 (arXiv:2507.12256v2 [quant-ph])
- **Affiliation**: Delft Institute of Applied Mathematics, Delft University of Technology (Delft, The Netherlands)
- **DOI / URL**: [arXiv:2507.12256](https://arxiv.org/abs/2507.12256)

---

## 2. Research Objective & Core Contribution
- **Objective**: Construct a low-depth, NISQ-compatible parameterized quantum circuit that directly implements the nonlinear, dissipative BGK collision operator without requiring ancilla post-selection, Carleman state dimension explosion, or multiple state copies.
- **Core Contribution**:
  - Introduces a **Surrogate Quantum Circuit (SQC)** acting purely locally on the 4-qubit velocity register of a D2Q9 lattice.
  - Imposes exact physical symmetries into the circuit ansatz:
    1. **Mass Conservation**: Automatically guaranteed by unitary norm preservation under rooted-density encoding.
    2. **Scale Equivariance**: Invariant under uniform multiplication of particle distributions.
    3. **$D_8$ Dihedral Group Equivariance**: Invariant under 8-fold lattice rotations ($\pi/2, \pi, 3\pi/2$) and reflections.
  - Compiles to **724 native gates** on the IBM Heron quantum processor.

---

## 3. Physical Model & State Encoding
- **Rooted-Density Amplitude Encoding** (Eq. 13):
  $$ |\psi\rangle = \frac{1}{\sqrt{M}} \sum_{\mathbf{x}, i} \sqrt{f_i(\mathbf{x}, t)} |\mathbf{e}_i\rangle \otimes |\mathbf{x}\rangle, \quad M = \sum_{\mathbf{x}, i} f_i(\mathbf{x}, t) $$
- **Local Single-Node Register** (Eq. 14):
  $$ |\psi_{node}\rangle = \frac{1}{\sqrt{\rho}} \sum_{i=0}^8 \sqrt{f_i} |\mathbf{e}_i\rangle, \quad \rho = \sum_{i=0}^8 f_i $$
- **Velocity Register**: 4 qubits ($2^4 = 16$ basis states: 9 physical D2Q9 states + 7 unphysical padded states).

---

## 4. Symmetry-Preserving Circuit Architecture
1. **Connectivity Invariance**: Two-qubit coupling graph is invariant under permutations of the $D_8$ group.
2. **Two Orbit Classes**:
   - Axial orbit (4 nearest-neighbor directions: $e_1, e_2, e_3, e_4$).
   - Diagonal orbit (4 corner directions: $e_5, e_6, e_7, e_8$).
   - Center rest state ($e_0$).
3. **Parametric Gate Layers**: Alternating layers of parameterized Single-Qubit Rotations ($R_x(\theta), R_z(\phi)$) and entangling two-qubit gates ($R_{zz}, \text{CZ}$) with weight sharing across symmetry orbits.

---

## 5. Loss Function & Training Routine
- **Loss Function**:
  $$ \mathcal{L}_{total} = \mathcal{L}_{MSE} + \lambda_{mom} \mathcal{L}_{mom} + \lambda_{leak} \mathcal{L}_{leak} $$
  where:
  - $\mathcal{L}_{MSE} = \frac{1}{N_{samples}} \sum_n \|\hat{\mathbf{f}}_{post} - \mathbf{f}_{BGK}^{eq}\|^2$
  - $\mathcal{L}_{mom} = \frac{1}{N_{samples}} \sum_n |\hat{\mathbf{j}} - \mathbf{j}_{true}|^2$ (penalizes momentum non-conservation)
  - $\mathcal{L}_{leak} = \sum_{k=9}^{15} |\langle k | \psi_{out} \rangle|^2$ (penalizes amplitude leakage into the 7 unphysical basis states).

---

## 6. Numerical Verification & Benchmarks
- Taylor-Green vortex decay ($Re = 10, 50, 100$).
- 2D Lid-driven cavity ($Re = 100, 400$).
- Matches classical kinetic energy decay rate and recirculation streamlines.

---

## 7. Key Relevance to Two-Phase Dam-Break QLBM
- **Compact Local Collision Alternative**: While Carleman linearization builds a global linear system for all time steps, the SQC offers a compact *local operator alternative* for the nonlinear BGK step that requires zero matrix inversion.
- **Phase-Field Coupling**: The same SQC ansatz can be trained on the phase-field chemical equilibrium $h_i^{eq}(\phi, \mathbf{u}, \mu_\phi)$, providing a learned quantum surrogate for interface dynamics.
- **Current Limitation**: In its basic form, SQC requires measurement and reinitialization between steps, unless chained with unitary streaming (as demonstrated by Nagel & Löwe 2025).
