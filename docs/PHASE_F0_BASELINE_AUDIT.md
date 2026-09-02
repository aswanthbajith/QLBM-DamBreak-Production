# PHASE F0: REPOSITORY BASELINE PROTECTION & AUDIT REPORT
## Pre-Phase F Quantum Collision & Parameter Oracle Integrity Record

**Document**: Repository Baseline Audit & Safety Verification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Dam-Break Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Base Commit**: `ce8e6f3`  
**Date**: September 2026  

---

## 1. Baseline Integrity Verification

1. **Active Branch**: `feature/direct-encoding-two-phase-qlbm`
2. **Current Base Commit**: `ce8e6f3` (*"QLBM Phase E: One-Node Quantum Collision Core, Parameterized Dilation, and Observable Readout Audit"*)
3. **Working Tree**: Clean (0 modified / 0 untracked files).
4. **Full Automated Test Suite**: **133 / 133 Passing (100%)** in $112.88\text{s}$.
5. **Frozen Level-6B Baseline**:
   - File: `quantum/level6b_hybrid_solver.py`
   - SHA-256 Checksum: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8`
   - Status: 100% Intact, Unmodified, and Verified.
6. **Original Research Archive Status**:
   - Location: `/home/aswa/Research/QLBM-DamBreak`
   - Branch: `master`
   - Status: 100% Intact, Untouched, and Clean.

---

## 2. Direct-Encoding Quantum Modules Overview

- [`quantum/direct_two_phase_prototype.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/direct_two_phase_prototype.py): Unified Hilbert space $\mathcal{H} = \mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$, direct state encoding/decoding, global unitary permutation streaming $S$, and boundary involution $B$.
- [`quantum/arithmetic_streaming.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/arithmetic_streaming.py): Reversible quantum gate-level arithmetic streaming circuits using modular ripple-carry adders/subtractors for D2Q9 velocities, and boundary involution circuits.
- [`quantum/one_node_collision.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/one_node_collision.py): One-node Level-4 classical reference, fixed linearized 6-qubit dilation $U_C$, state-dependent parameterized 6-qubit dilation $U_C(\alpha, \mathbf{u})$, and quantum observable readout (Hadamard overlap test).

---

## 3. Current Scientific Status & Limitations

1. **State Representation**: populations $f_i, g_i$ are encoded linearly in basis state amplitudes $|x,y,i,p\rangle$. Measurement probabilities are $P(x,y,i,p) = a^2 / \mathcal{N}^2$.
2. **Current Spatial Prototype**: Currently executes in a hybrid quantum-classical loop where macroscopic quantities $(\rho, \alpha, \mathbf{u})$ and spatial CSF forces are computed classically on CPU.
3. **Phase F Objective**: Develop a canonical Level-4 reference (`quantum/reference_collision.py`), thoroughly audit parameterized collision matrices across a deterministic parameter sweep, investigate coherent vs hybrid parameter handling (Phase F3/F4), and validate one-node parameterized quantum collision dilation (Phase F5).
