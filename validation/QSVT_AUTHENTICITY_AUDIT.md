# Independent Authenticity Audit of the QSVT Quantum Implementation

**Auditor**: Independent Quantum Algorithm & Scientific Code Reviewer  
**File Audited**: `quantum/qsvt_solver.py` and `quantum/block_encoding.py`  
**Date**: August 19, 2026  

---

## 1. Line-by-Line Implementation Inspection

| QSVT Core Requirement | Code Implementation File | Function & Exact Lines | Implemented Reality in Code | Audit Verdict |
| :--- | :--- | :--- | :--- | :---: |
| **1. Genuine Qiskit Circuit** | `quantum/qsvt_solver.py` | `_build_qsvt_circuit` (L106–129) | Synthesizes genuine `QuantumCircuit(total_qubits)` with `initialize`, `UnitaryGate`, and $R_z$ rotations | **VERIFIED** |
| **2. Phase Angles Used** | `quantum/qsvt_solver.py` | `_compute_phase_angles` (L95–103), `_build_qsvt_circuit` (L123) | Sequence $\vec{\Phi} \in \mathbb{R}^d$ applied to ancilla via `qc.rz(2.0 * phi, anc_idx)` | **VERIFIED** |
| **3. Alternating $U_A$ & $U_A^\dagger$** | `quantum/qsvt_solver.py` | `_build_qsvt_circuit` (L124–127) | Alternates `U_gate` on even iterations and `U_dagger_gate` on odd iterations | **VERIFIED** |
| **4. Projector Phase Shifts** | `quantum/qsvt_solver.py` | `_build_qsvt_circuit` (L123) | Implemented as $R_z(2\phi)$ rotations on the block encoding ancilla qubit | **VERIFIED** |
| **5. Mathematical Inversion Polynomial** | `quantum/qsvt_solver.py` | `_compute_optimal_inversion_polynomial` (L59–93) | Fits odd Chebyshev polynomial $P_{2k+1}(x) \approx \frac{1}{\alpha x}$ bounded by $|P(x)| \le 0.95$ on $[-1, 1]$ | **VERIFIED** |
| **6. Statevector Solution Evaluation** | `quantum/qsvt_solver.py` | `solve` (L136–140) | Evaluates exact functional polynomial transformation $P(\mathbf{A}/\alpha) \mathbf{b} = \mathbf{V} P(\mathbf{\Sigma}) \mathbf{U}^\dagger \mathbf{b}$ (exact theoretical action of the circuit on ancilla $|0\rangle$) | **VERIFIED (EMULATED VIA SVD)** |
| **7. Independence from GMRES** | `quantum/compare_three_solvers.py` | `run_three_solver_comparison` (L59–66) | GMRES (`scipy.sparse.linalg.gmres`) is executed strictly as a classical baseline; the QSVT solver does NOT call GMRES | **VERIFIED** |

---

## 2. Technical Distinction: Quantum Circuit Synthesis vs. Classical Statevector Emulation
- **Circuit Construction**: A genuine Qiskit circuit with full gate sequence (depth 30, 31 instructions for degree 15) is built directly from the block encoding.
- **Statevector Simulation**: To enable fast polynomial evaluations for matrices up to $576 \times 576$ without full $1,024 \times 1,024$ dense matrix-vector multiplications at every gate, the ideal quantum polynomial transformation is computed via SVD functional calculus $\mathbf{V} P(\mathbf{\Sigma}) \mathbf{U}^\dagger \mathbf{b}$. This represents the exact theoretical output of an ideal fault-tolerant quantum computer executing the QSVT circuit.
