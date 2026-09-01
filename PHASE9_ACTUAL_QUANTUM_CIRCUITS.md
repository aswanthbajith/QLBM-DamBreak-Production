# PHASE 9 ACTUAL QUANTUM CIRCUIT INVENTORY (STAGE 9.2)

**Status**: Verified Qiskit QuantumCircuit Object Registry  
**Date**: 2026-08-19  

---

## 1. Explicit QuantumCircuit Objects in Repository

| Circuit ID | File & Line | Name | Qubits ($n_{\text{tot}}$) | Ancillas | Operations | Classical Bits | Measurements | Transpilable | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`QC_U_A_BLOCK_ENC`** | `quantum/block_encoding.py:70` | `U_A` | $1 + \lceil \log_2(D_C) \rceil$ | 1 | `UnitaryGate(U_matrix)` (for $n \le 8$) / `Gate` (for $n > 8$) | 0 | None | Yes | **REAL_CIRCUIT ($n \le 8$)** |
| **`QC_QSVT_INVERSION`**| `quantum/qsvt_solver.py:114` | `QSVT_Inversion` | $1 + \lceil \log_2(D_C) \rceil$ | 1 | `Initialize(|b>)`, alternating $R_z(2\phi_j)$ and $U_A / U_A^\dagger$ | 0 | None | Yes | **REAL_CIRCUIT ($n \le 8$)** |

---

## 2. Technical Findings
1. **Explicit Gate Materialization ($n \le 8$)**: For circuits on 8 or fewer total qubits (e.g. toy models, $N=1$ reduced subsystems, 2-to-8 qubit benchmarks), full Qiskit `UnitaryGate` objects are instantiated and can be transpiled directly to native hardware basis gates (`cx`, `sx`, `rz`, `x`).
2. **Opaque Gate Representation ($n > 8$)**: For $n > 8$ qubits ($N=1, D_C=342 \implies 10$ qubits; $N=8, D_C=2,736 \implies 13$ qubits; $N=30,000 \implies 25$ qubits), Qiskit uses high-level un-decomposed `Gate` placeholders to avoid exponential classical decomposition costs.
