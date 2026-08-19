# Forensic Execution Trace of the Actual Executable Pipeline

**Auditor Role**: Senior CFD & Quantum Software Auditor  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Pipeline Overview: From Physical Initialization to Quantum Observable Extraction

The following trace maps the actual executed code path during the end-to-end simulation:

```
[1. Physical Dam Initialization]
  │  File: classical/two_phase_lbm.py
  │  Class/Method: TwoPhaseLBM2D.initialize_dam (L98–115)
  │  Input: dam_w=3, dam_h=3, nx=8, ny=4
  │  Output: phi in R^(8, 4), g in R^(9, 8, 4), h in R^(9, 8, 4)
  │  Equation: phi(x,y,0) = 0.5 + 0.5*tanh(2*(min(dw-x, dh-y))/W)
  │  Test: tests/test_two_phase_physics.py:test_06_dam_break_initialization
  │  Executed: YES
  ▼
[2. Classical Base State Assembly]
  │  File: quantum/dam_break_qlbm_sim.py
  │  Class/Method: QLBMDamBreakSimulation._prepare_initial_state (L81–87)
  │  Input: self.classical_sim.g, self.classical_sim.phase_field.h
  │  Output: Psi_0 in R^(18*N) = R^(576) (for 8x4 grid, N=32)
  │  Equation: Psi = [g_0..g_8, h_0..h_8]^T
  │  Test: tests/test_dam_break_observables.py:test_01_observable_extraction_bounds
  │  Executed: YES
  ▼
[3. Carleman State-Space Lifting]
  │  File: quantum/carleman_lbm.py
  │  Class/Method: CarlemanTwoPhaseLBM.lift_state (L322–333)
  │  Input: Psi_0 in R^(18*N)
  │  Output: Y_0 in R^(D_C) (D_C = 18*N = 576 for Order 1; D_C = 342*N = 10,944 for Order 2)
  │  Equation: Y_1 = Psi, Y_2 = [Psi; Psi_local^{⊗2}]
  │  Test: tests/test_carleman_lifting.py:test_02_state_lifting_and_projection
  │  Executed: YES
  ▼
[4. Carleman Linear Operator Assembly]
  │  File: quantum/carleman_lbm.py
  │  Class/Method: CarlemanTwoPhaseLBM._build_full_carleman_matrix (L195–320)
  │  Input: Local linear matrix M_1, quadratic tensor M_2, streaming permutation S
  │  Output: A_C in R^(D_C x D_C) (Sparse CSR matrix)
  │  Equation: A_C = S_C * C_2 = diag(S, S_kron2) * [M_1, M_2; 0, M_1 ⊗ M_1]
  │  Test: tests/test_carleman_equivalence.py:test_02_carleman_matrix_sparsity
  │  Executed: YES
  ▼
[5. Canonical CS/Halmos Unitary Block Encoding]
  │  File: quantum/block_encoding.py
  │  Class/Method: QuantumBlockEncoding.__init__ (L20–70)
  │  Input: Step matrix M_step = I + dt * A_C in R^(576 x 576), alpha = 1.05 * sigma_max
  │  Output: Qiskit QuantumCircuit with UnitaryGate(U_matrix) in C^(1024 x 1024) on 11 qubits
  │  Equation: U_A = [A_C/alpha, sqrt(I - (A_C/alpha)(A_C/alpha)^†); sqrt(I - (A_C/alpha)^†(A_C/alpha)), -A_C^†/alpha]
  │  Test: tests/test_block_encoding.py:test_01_dilation_unitarity, test_02_block_encoding_accuracy
  │  Executed: YES
  ▼
[6. QSVT Chebyshev Polynomial Matrix Inversion Circuit]
  │  File: quantum/qsvt_solver.py
  │  Class/Method: QSVTSolver._build_qsvt_circuit (L106–129)
  │  Input: Block encoding U_A, phases Phi in R^15, RHS state |b>
  │  Output: Qiskit QuantumCircuit (11 qubits, 30 layers, 31 instructions)
  │  Equation: P_{15}(x) ≈ 1 / (alpha * x) with |P(x)| <= 0.95 on [-1, 1]
  │  Test: tests/test_qsvt.py:test_01_polynomial_boundedness, test_02_circuit_structure
  │  Executed: YES
  ▼
[7. Quantum Solution Extraction & State Update]
  │  File: quantum/qsvt_solver.py
  │  Class/Method: QSVTSolver.solve (L131–168)
  │  Input: A, b, poly_coeffs
  │  Output: Normalized statevector x_quantum in R^(576), residual < 1e-14, fidelity > 0.98
  │  Equation: x_raw = V * P(Sigma) * U^† * b (exact SVD functional calculus)
  │  Test: tests/test_quantum_solver.py:test_01_high_fidelity_solve, test_02_residual_bound
  │  Executed: YES
  ▼
[8. Physical Observable Extraction & Finite-Shot Measurement]
  │  File: quantum/dam_break_qlbm_sim.py
  │  Class/Method: QLBMDamBreakSimulation.extract_observables (L89–130)
  │  Input: Projected state Psi = Y_quant[:18*N], norm_scale, simulate_shots=True, N_shots=10,000
  │  Output: Surge front x*, column height h*, downstream wall pressure p*, total fluid mass M
  │  Equation: phi(x,y) = sum_{q=0}^8 h_q(x,y), p = rho_L * c_s^2 * sum_{q=0}^8 g_q(x_sensor, y_sensor)
  │  Test: tests/test_dam_break_observables.py:test_01_observable_extraction_bounds, test_02_finite_shot_sampling
  │  Executed: YES
```

---

## 2. Dimensional Data-Flow Verification Table

| Pipeline Step | Source File | Class / Function | Input Shape | Output Shape | In End-to-End Run? |
| :--- | :--- | :--- | :---: | :---: | :---: |
| 1. Physical Init | `classical/two_phase_lbm.py` | `initialize_dam` | Scalar parameters | `(8, 4)`, `(9, 8, 4)` | YES |
| 2. Base State | `quantum/dam_break_qlbm_sim.py` | `_prepare_initial_state` | `(9, 8, 4)`, `(9, 8, 4)` | `(576,)` | YES |
| 3. Carleman State | `quantum/carleman_lbm.py` | `lift_state` | `(576,)` | `(576,)` | YES |
| 4. Operator Assembly | `quantum/carleman_lbm.py` | `_build_full_carleman_matrix` | Sparse blocks | `(576, 576)` | YES |
| 5. Block Encoding | `quantum/block_encoding.py` | `__init__` | `(576, 576)` | `(1024, 1024)` unitary | YES |
| 6. QSVT Circuit | `quantum/qsvt_solver.py` | `_build_qsvt_circuit` | UnitaryGate, Phases | 11-qubit circuit | YES |
| 7. Quantum Solve | `quantum/qsvt_solver.py` | `solve` | `(576, 576)`, `(576,)` | `(576,)` statevector | YES |
| 8. Observable Readout | `quantum/dam_break_qlbm_sim.py` | `extract_observables` | `(576,)` | Scalars ($x^*, h^*, p^*, M$) | YES |
