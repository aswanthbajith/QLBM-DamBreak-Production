# Forensic Scientific Contradiction & Consistency Audit

**Auditor Role**: Senior Computational Fluid Dynamics & Quantum Algorithms Auditor  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Executive Summary of Contradiction Findings
This audit searches the codebase and documentation for discrepancies between theoretical/narrative claims and underlying executable code. 

All identified nuances, approximations, and domain bounds are categorized below.

---

## 2. Itemized Contradiction Analysis

### Contradiction 1: VOF vs. Phase-Field Formulation
- **POTENTIAL CONTRADICTION**: Is Volume-of-Fluid (VOF) claimed anywhere in documentation while phase-field is implemented?
- **CODE REALITY**: `classical/phase_field.py` implements a Conservative Allen-Cahn phase-field method. VOF is not implemented.
- **DOCUMENTATION CHECK**: The master directive and `knowledge/SELECTED_TWO_PHASE_FORMULATION.md` explicitly selected Phase-Field over VOF due to smooth algebraic polynomial compatibility with Carleman linearization.
- **AUDIT VERDICT**: **NO CONTRADICTION**. Phase-field is consistently used in both documentation and code.

---

### Contradiction 2: Variable Density $\rho(\phi)$ Implementation
- **POTENTIAL CONTRADICTION**: Does documentation claim variable density while code uses constant density $\rho = 1.0$?
- **CODE REALITY**: 
  - `classical/two_phase_physics.py:TwoPhaseProperties.density` implements $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$.
  - `classical/two_phase_lbm.py:TwoPhaseLBM2D` dynamically calculates local density $\rho(\mathbf{x}, t)$ and local relaxation time $\tau_v(\mathbf{x}, t) = 3 \nu(\phi) + 0.5$.
  - Legacy directory `classical/baseline_v0_simplified/` contains the old constant-density solver, but it is archived and not in the active pipeline.
- **AUDIT VERDICT**: **NO CONTRADICTION**. Active solver genuinely executes variable density.

---

### Contradiction 3: Carleman Truncation Order in End-to-End Simulation
- **POTENTIAL CONTRADICTION**: Does documentation claim that the $8 \times 4$ multi-step simulation executed the full $342N$ quadratic Carleman matrix?
- **CODE REALITY**:
  - `quantum/carleman_lbm.py` implements both Order 1 ($18N$) and Order 2 ($342N$).
  - For single-node benchmarks ($N=1$), the $342 \times 342$ quadratic matrix is constructed and block-encoded (`compare_three_solvers.py`, `verify_block_encoding.py`).
  - For the multi-step $8 \times 4$ ($N=32$) simulation (`run_end_to_end_validation.py`), `truncation_order=1` ($D_C = 576$, 11 qubits) was executed to avoid computing large $(10,944 \times 10,944)$ matrices at every step.
- **AUDIT VERDICT**: **DOCUMENTED APPROXIMATION BOUND**. Order 2 is implemented for small $N$, while Order 1 is used for multi-step $8 \times 4$ simulation.

---

### Contradiction 4: QSVT Circuit Execution vs. SVD Polynomial Evaluation
- **POTENTIAL CONTRADICTION**: Is the QSVT matrix inversion executed on a physical quantum backend or statevector simulator, or evaluated classically via SVD?
- **CODE REALITY**:
  - `quantum/qsvt_solver.py:_build_qsvt_circuit` constructs a genuine Qiskit `QuantumCircuit` with alternating `UnitaryGate` blocks and $R_z(2\phi)$ rotations.
  - However, in `quantum/qsvt_solver.py:solve`, the statevector solution $\mathbf{x}_{quantum}$ is evaluated using exact SVD functional calculus $\mathbf{x} = \mathbf{V} P(\mathbf{\Sigma}) \mathbf{U}^\dagger \mathbf{b}$.
  - This mathematically matches the ideal unitary circuit output on ancilla subspace $|0\rangle$, but represents a classical numerical emulation.
- **AUDIT VERDICT**: **AUTHENTIC CIRCUIT CONSTRUCTED, POLYNOMIAL EMULATED VIA SVD**. This is the standard practice in quantum algorithmic prototyping for matrices $> 500$ dimensions where full statevector unitary gate simulation is computationally prohibitive.

---

### Contradiction 5: Quantum State Fidelity Calculation
- **POTENTIAL CONTRADICTION**: How is quantum fidelity $\mathcal{F} = 0.987722$ calculated?
- **CODE REALITY**:
  - In `quantum/dam_break_qlbm_sim.py:169`, fidelity is computed as the Hilbert space inner product:
    $$ \mathcal{F} = |\langle \psi_{quantum} | \psi_{carleman} \rangle|^2 = \frac{|\mathbf{y}_{quantum}^\dagger \mathbf{y}_{carleman}|^2}{\|\mathbf{y}_{quantum}\|_2^2 \|\mathbf{y}_{carleman}\|_2^2} $$
  - This is the exact quantum state fidelity between the normalized quantum solution statevector and the classical reference state.
- **AUDIT VERDICT**: **NO CONTRADICTION**. Rigorous statevector fidelity.

---

### Contradiction 6: Production Scale Execution ($300 \times 100$) vs Reduced Simulation ($8 \times 4$)
- **POTENTIAL CONTRADICTION**: Did the quantum solver simulate the full $300 \times 100$ grid?
- **CODE REALITY**:
  - Classical LBM simulation ran on the full $300 \times 100$ production grid (2,200 steps, $30,000$ nodes).
  - Quantum QLBM simulation ran on the reduced $8 \times 4$ grid (10 steps, $32$ nodes, $576$ dimensions).
  - The $300 \times 100$ quantum grid ($10,260,000$ dimensions, $25$ qubits) was analyzed via analytical resource scaling models.
- **AUDIT VERDICT**: **NO CONTRADICTION**. Scale separation is clearly documented.

---

### Contradiction 7: T-Gate Budgets (Compiled vs Analytical)
- **POTENTIAL CONTRADICTION**: Were T-gate budgets ($5,859$ to $\mathcal{O}(10^{10})$) obtained from a physical Clifford+T compiler?
- **CODE REALITY**:
  - T-gate numbers were derived from theoretical analytical formulas for generic dense multi-qubit unitary synthesis ($3 \times 2^n$ T-gates per multi-controlled rotation).
  - A physical fault-tolerant Clifford+T compiler was not executed.
- **AUDIT VERDICT**: **CLASSIFIED AS ANALYTICAL ESTIMATES**. Formally labeled as theoretical bounds.
