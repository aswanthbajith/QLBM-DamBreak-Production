# PHASE F20: CONTINUUM SURFACE FORCE (CSF) ANALYSIS

## 1. Physical Surface Tension Formulation
In two-phase Lattice Boltzmann hydrodynamics, the interfacial surface tension force is modeled using the Continuum Surface Force (CSF) approach:
$$\mathbf{F}_{\text{CSF}} = \sigma \kappa \nabla \alpha$$
where:
- $\sigma$ is the surface tension coefficient ($\sigma = 0.001$ in the validated physical benchmark),
- $\nabla \alpha = \left( \frac{\partial \alpha}{\partial x}, \frac{\partial \alpha}{\partial y} \right)^T$ is the interface normal gradient,
- $\kappa = -\nabla \cdot \mathbf{n} = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$ is the local interface curvature.

---

## 2. Four-Tier Architectural Classification
To maintain absolute scientific transparency, CSF implementation is classified across four distinct tiers:

From [`results/phase_f20/f20_csf.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_csf.csv):

### Tier 1: Classical CSF (Level-4 Ground Truth)
- Evaluates $\nabla \alpha$ and $\kappa$ on the classical host using standard 9-point isotropic finite-difference stencils with zero-flux solid boundary conditions.
- Status: **VALIDATED & RUNNING** in [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py).
- Serves as the numerical ground-truth benchmark for all dam-break experiments.

### Tier 2: Quantum-Compatible Oracle (Level-6B Baseline)
- Classical host computes the local curvature $\kappa(\mathbf{x})$ and interface gradient $\nabla \alpha(\mathbf{x})$ at each timestep $t$.
- Injects $\mathbf{F}_{\text{CSF}}$ into the quantum circuit via an external parameter bus / rotational oracle feeding the local collision registers.
- Status: **VALIDATED & FROZEN** in [`quantum/level6b_hybrid_solver.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/level6b_hybrid_solver.py).

### Tier 3: Reversible Arithmetic CSF (FTQC Blueprint)
- Evaluates $\nabla \alpha$ using inter-node subtraction circuits and evaluates curvature $\kappa$ using fixed-point reciprocal square-root and divergence circuits on quantum registers.
- Estimated resource cost: $\approx 18,500$ Toffoli gates per node.
- Status: **MATHEMATICALLY FEASIBLE BUT UNIMPLEMENTED AT GATE LEVEL**.

### Tier 4: Fully Autonomous Quantum CSF
- End-to-end unitary evaluation of non-local spatial curvature stencils across quantum wires without measurement or external classical communication.
- Estimated cost: $> 25,000$ Toffolis per node and high circuit depth.
- Status: **THEORETICAL ARCHITECTURE ONLY**.

---

## 3. Truth-in-Advertising Verdict
The project does **NOT** claim Tier 4 autonomous quantum CSF.
In the autonomous quantum circuit demonstrator, $\sigma = 0$ in the gate-level reversible arithmetic, while qualitative surface pinning is modeled via controlled-phase (CZ) gates. Full physical surface tension ($\sigma = 0.001$) is validated exclusively in the Tier 1 reference and Tier 2 Level-6B hybrid solver.
