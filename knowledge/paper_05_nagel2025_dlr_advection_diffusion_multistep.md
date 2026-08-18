# Knowledge Base Dossier: Nagel & Löwe (DLR, 2025)

## 1. Citation & Metadata
- **Title**: Quantum Lattice Boltzmann Method for Multiple Time Steps Without Reinitialization for Linear Advection-Diffusion Problems
- **Authors**: Aaron Nagel, Johannes Löwe
- **Year**: Oct 7, 2025 (arXiv:2510.05965v1 [physics.flu-dyn])
- **Affiliation**: German Aerospace Center (DLR), Institute of Aerodynamics and Flow Technology (Göttingen, Germany)
- **DOI / URL**: [arXiv:2510.05965](https://arxiv.org/abs/2510.05965)

---

## 2. Research Objective & Core Contribution
- **Objective**: Eliminate the need for mid-circuit measurements, state tomography, and classical reinitialization between simulation time steps in Quantum Lattice Boltzmann Methods.
- **Core Contribution**:
  - Develops a multi-time-step QLBM algorithm where state evolution (collision $\to$ streaming $\to$ macroscopic aggregation $\to$ re-preparation) occurs entirely on the quantum circuit across all $T$ time steps.
  - Removes the linear-in-grid-size measurement cost $\mathcal{O}(N)$ between steps, preserving end-to-end quantum advantage.
  - Demonstrates that global scalar target observables (e.g. total volume fraction, interface center of mass, drag/lift) can be evaluated at the end of $T$ steps without ever extracting the full spatial flow field.
  - Explicitly derives quantum gate diagrams and validates using Qiskit shot-based noisy and ideal simulators.

---

## 3. Physical Model & Governing PDEs
- **Scalar Advection-Diffusion Equation** (Eq. 1):
  $$ \frac{\partial \Phi}{\partial t} + u_j \frac{\partial \Phi}{\partial x_j} = D \frac{\partial^2 \Phi}{\partial x_j^2} $$
  where $\Phi$ is a transported scalar field (identical in form to the phase field order parameter $\phi$ in two-phase flows), $u_j$ is the advection velocity, and $D$ is the diffusion coefficient.

---

## 4. Lattice Model & Equilibrium Formulation
- **Lattices**: D1Q3 (1D 3-velocity: $e_i \in \{0, +1, -1\}$) and D2Q5 / D2Q9 (2D).
- **Linear Equilibrium Distribution** (Eq. 5):
  $$ f_i^{eq} = w_i \Phi \left( 1 + \frac{e_{ij} u_j}{c_s^2} \right) $$
  Linear in the transported scalar $\Phi$, requiring no Carleman expansion for constant or advective transport.

---

## 5. Multi-Step Quantum Circuit Architecture
1. **Quantum Registers**:
   - Spatial register $|\mathbf{x}\rangle = |x_1 x_2 \dots x_n\rangle$.
   - Velocity direction register $|i\rangle$.
   - Ancilla work qubits for unitary arithmetic.
2. **Unitary Collision Block**:
   - Rotates local populations toward equilibrium using controlled Givens/Y-rotations.
3. **Unitary Streaming Block**:
   - Spatial coordinate incrementer/decrementer circuits acting on the spatial register conditioned on the velocity register.
4. **Macroscopic Projection & Re-Preparation**:
   - Projects distribution populations back into the scalar state $|\Phi\rangle$ using unitary aggregation and prepares the next time-step input state purely coherently without measurement.

---

## 6. Amplitude Decay & Quantum Efficiency Bounds
- **State Amplitude Decay**:
  Because the collision operation involves non-unitary sub-blocks embedded into larger unitaries, the success amplitude $\gamma_t$ decays as $\gamma_t \sim \gamma_0^t$.
- **Mitigation**:
  Analyzes amplitude amplification and thresholding limits to determine maximum feasible multi-step depth $T_{max}$ on NISQ/FTQC architectures.

---

## 7. Direct Application to Two-Phase Dam-Break QLBM
- **Direct Match for Phase-Field Equation**: The conservative Allen-Cahn interface equation for the dam-break order parameter $\phi$ has the exact mathematical structure:
  $$ \frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot (M \nabla \phi) + \text{source} $$
  Nagel & Löwe's measurement-free multi-step QLBM circuit can be adopted directly as the **Quantum Phase-Field Interface Propagator** within our coupled two-phase dam-break framework!
