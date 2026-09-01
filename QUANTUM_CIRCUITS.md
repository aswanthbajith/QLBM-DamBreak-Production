# QUANTUM CIRCUITS SPECIFICATION & GATE-LEVEL PROFILES

This document contains the concrete circuit architectures, gate counts, depth, and connectivity specifications for each quantum component in `QLBM-DamBreak-Production`.

---

## 1. Inventory of Quantum Circuits

| # | Quantum Circuit | Logical Qubits | Ancillas | Total Qubits | Gate Types | Circuit Depth | 2-Qubit CX/ECR | Measurements |
| :-: | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| 1 | **State Preparation** (`qc_sp`) | 9 | 0 | 9 | $R_y$, $R_z$, CX | 1 (isometry) | $\le 512$ | 0 |
| 2 | **Carleman Block Encoding** (`qc_collision`) | 9 | 1 | 10 | UnitaryGate / QSD | 1 (dense) | 21,133 (transpiled) | 1 (postselection) |
| 3 | **Buoyancy Forcing Dilation** (`qc_force`) | 9 | 1 | 10 | UnitaryGate / Affine | 1 (dense) | 18,450 (transpiled) | 1 (postselection) |
| 4 | **Spatial Streaming Permutation** (`qc_stream`) | 9 | 0 | 9 | Modular Increment / Swap | 1 (unitary) | 4,200 (transpiled) | 0 |
| 5 | **Boundary Bounce-Back** (`qc_boundary`) | 9 | 0 | 9 | Multi-Controlled Swap | 1 (involution) | 3,150 (transpiled) | 0 |
| 6 | **Velocity Observable Operator** (`qc_observable`) | 9 | 1 | 10 | Hadamard, Controlled-$C_x/C_y$ | 3 | 18 | 1 |
| 7 | **Unified Timestep** (`QuantumDamBreakStep`) | 9 | 1 | 10 | Composite | 6 | 76,459 (transpiled) | 1 |

---

## 2. Gate-Level Circuit Diagrams & Decompositions

### A. State Preparation Circuit (`qc_sp`)
```text
q0_x0: ──[StatePreparation(ψ0)]──
q1_x1: ──[                      ]──
q2_y0: ──[                      ]──
q3_y1: ──[                      ]──
q4_v0: ──[                      ]──
q5_v1: ──[                      ]──
q6_v2: ──[                      ]──
q7_v3: ──[                      ]──
q8_sel: ──[                      ]──
```

### B. Carleman Block Encoding Dilation Circuit (`qc_collision`)
```text
anc_0:  ──|0⟩──[                             ]──M── [Postselect |0⟩]
q0..q8: ──|Ψ⟩──[ Carleman Dilation U_C (10Q) ]────── |Ψ*⟩ / α
```
* **Matrix Dimension**: $1024 \times 1024$.
* **Unitarity**: Verified $\|U_C^\dagger U_C - I_{1024}\|_2 = 3.50 \times 10^{-14}$.
* **Transpiled Heavy-Hex Depth**: 76,459 gates (21,133 two-qubit CX gates).

### C. Reversible Spatial Streaming Circuit ($S$)
```text
q_x: ────[ + cx(v) mod Nx ]────
q_y: ────[ + cy(v) mod Ny ]────
q_v: ──────────■───────────────
q_s: ──────────────────────────
```
* **Permutation Dimension**: $512 \times 512$.
* **Unitarity**: Exact $\|S^\dagger S - I_{512}\|_2 = 0.000000$.

### D. Boundary Bounce-Back Involution Circuit ($B$)
```text
q_x: ────■──(x in {0, Nx-1})────
q_y: ────■──(y in {0, Ny-1})────
q_v: ────X──[ v <-> opp(v) ]────
q_s: ───────────────────────────
```
* **Involution Dimension**: $512 \times 512$.
* **Involution Property**: Exact $B^2 = I_{512}, B^\dagger B = I_{512}$.

### E. Unified Full Timestep Circuit Architecture
```text
|0⟩_anc: ──[ U_collision ]──M──[ U_force ]──M─────── |0⟩_anc
|Ψ_t⟩:   ──[             ]─────[         ]────[ S ]────[ B ]── |Ψ_{t+1}⟩
```

---

## 3. IBM Quantum Heavy-Hex 127Q Transpilation Profile

* **Target Device**: IBM Quantum 127Q Heavy-Hex (`generic_backend_127q`).
* **Basis Gates**: `['cx', 'id', 'rz', 'sx', 'x']` / `['ecr', 'id', 'rz', 'sx', 'x']`.
* **Coupling Map**: Heavy-Hex connectivity graph with 127 physical nodes.
* **Transpiler Optimization Level**: 2.
* **Transpilation Execution Time**: 1.14 s.
