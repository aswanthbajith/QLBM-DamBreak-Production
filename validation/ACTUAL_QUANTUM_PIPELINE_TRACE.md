# Line-by-Line Execution Trace of Actual Quantum LBM Dam-Break Pipeline

**Audit Date**: August 19, 2026  
**Auditor**: Independent Quantum Algorithm & Scientific Code Reviewer  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Complete End-to-End Pipeline Execution Flow

```
[1. Dam-Break Initial Condition]
  File: classical/two_phase_lbm.py:initialize_dam (L98-115)
  Dimension: phi in R^(Nx x Ny), g in R^(9 x Nx x Ny), h in R^(9 x Nx x Ny)
  Input: dam_w, dam_h
  Output: Smooth tanh liquid column and equilibrium distributions g_eq, h_eq
       │
       ▼
[2. LBM State Assembly]
  File: quantum/dam_break_qlbm_sim.py:_prepare_initial_state (L81-87)
  Dimension: Psi_0 in R^(18 N) (18N = 576 for 8x4 grid)
  Input: g, h distributions
  Output: Flattened base state vector Psi_0
       │
       ▼
[3. Carleman State Lifting]
  File: quantum/carleman_lbm.py:lift_state (L322-333)
  Dimension: For N_C=1: Y_0 in R^(18 N) (dim 576). For N_C=2: Y_0 in R^(342 N) (dim 10,944).
  Input: Psi_0 in R^(18 N)
  Output: Lifted Carleman state Y_0
       │
       ▼
[4. Matrix Operator Assembly (A_C)]
  File: quantum/carleman_lbm.py:_build_full_carleman_matrix (L195-320)
  Dimension: A_C in R^(18N x 18N) for N_C=1 (576 x 576); R^(342N x 342N) for N_C=2 (10,944 x 10,944).
  Input: Local collision M1, quadratic tensor M2, streaming permutation S
  Output: Sparse CSR matrix A_C = S_C * C_2
       │
       ▼
[5. Canonical Unitary Block Encoding]
  File: quantum/block_encoding.py:QuantumBlockEncoding (L20-70)
  Dimension: Unitary U_A in C^(2d x 2d) on (n_sys + 1) qubits (1,024 x 1,024 for 576-dim; 11 qubits)
  Input: Linear system matrix M_step = I + 0.01 * A_C
  Output: Qiskit QuantumCircuit with UnitaryGate(U_matrix) satisfying <0|U_A|0> = M_step / alpha
       │
       ▼
[6. QSVT Matrix Inversion Sequence]
  File: quantum/qsvt_solver.py:QSVTSolver (L16-130)
  Dimension: Circuit on 11 qubits with degree d=15 alternating sequence (depth 30, 31 instructions)
  Input: U_A, U_A_dagger, phase sequence Phi in R^15, initial state |b>
  Output: Qiskit QuantumCircuit and SVD functional calculus polynomial transformation P(M/alpha) ~ M^(-1)
       │
       ▼
[7. Quantum Solution State Extraction]
  File: quantum/qsvt_solver.py:solve (L131-168)
  Dimension: Normalized statevector x_quantum in R^576
  Input: QSVT polynomial evaluation on state
  Output: Optimal scaled quantum solution state vector Y_quant
       │
       ▼
[8. Physical Observable Extraction & Measurement]
  File: quantum/dam_break_qlbm_sim.py:extract_observables (L89-130)
  Dimension: Macroscopic scalar observables
  Input: Projected state Psi = Y_quant[:18N]
  Output: Surge front x*, column height h*, pressure p*, mass M, with simulated finite-shot noise (N_shots=10,000)
```

---

## 2. Dimensional Trace Summary for 8x4 Grid ($N=32$)
- **Base Grid Nodes $N$**: $8 \times 4 = 32$
- **Base LBM Populations ($9g + 9h$)**: $18 \times 32 = \mathbf{576}$
- **Carleman Order 1 Dimension**: $\mathbf{576}$
- **Carleman Order 2 Quadratic Dimension**: $342 \times 32 = \mathbf{10,944}$
- **Block Encoding Matrix Dimension ($2^n \times 2^n$)**: $\mathbf{1,024 \times 1,024}$ ($n_{sys}=9 \implies 2^9=512$, padded to $2^{10}=1,024$)
- **Total Qubits in Qiskit Circuit**: $\mathbf{11}$ ($10$ system qubits $+ 1$ ancilla)
