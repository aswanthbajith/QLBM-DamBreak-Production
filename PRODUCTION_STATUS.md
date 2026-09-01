# QLBM DAM-BREAK PRODUCTION STATUS REPORT

**Status Date**: September 2026  
**Implementation**: Hybrid Quantum-Classical Carleman Lattice Boltzmann Solver (Production)  
**Location**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Scientific Verdict**: **PRODUCTION READY WITH SCIENTIFIC QUALIFICATIONS**  

---

## 1. Executive Summary

The production repository has been audited, corrected, and frozen around the verified **Hybrid Local Carleman QLBM** pipeline with strictly separated and independently unitary quantum operators:

1. **Independent State Encoding (`quantum/two_phase_encoding.py`)**: Local 18-component vector $\Psi = [f_0..f_8, g_0..g_8]^T \in \mathbb{R}^{18}$ encoded with selector $s=0 \to f_i$, $s=1 \to g_i$. The phase qubit is not treated as a physical macroscopic phase field.
2. **Local Second-Order Carleman Truncation (`quantum/two_phase_carleman.py`)**: Step-evaluation map $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$. The quadratic lift $\mathbf{Y}_2 = [\Psi; \Psi \otimes \Psi]$ is rebuilt each timestep from measured physical populations.
3. **10-Qubit Power-of-Two Unitary Dilation (`quantum/unitary_dilation.py`)**: $A_{\text{eval}}$ is padded to $512 \times 512$ ($2^9$) and dilated to $U_C \in \mathbb{U}(1024 = 2^{10})$ ($\|U_C^\dagger U_C - I\| = 3.50 \times 10^{-14}$).
4. **Reversible Spatial Streaming Permutation $S$ (`quantum/streaming.py`)**: Exact 512-dimensional permutation operator on the full 9-qubit Hilbert space ($\|S^\dagger S - I_{512}\| = 0.000000$).
5. **Direction-Selective Boundary Bounce-Back Involution $B$ (`quantum/two_phase_boundary.py`)**: Exact 512-dimensional orthogonal involution ($B = B^\dagger, B^2 = I_{512}, \|B^\dagger B - I_{512}\| = 0.000000$).
6. **Spatial Composition**: $U_{\text{spatial}} = B \cdot S$ is strictly unitary across all 512 basis states ($\|U_{\text{spatial}}^\dagger U_{\text{spatial}} - I_{512}\| = 0.000000$).
7. **Hybrid Simulation Loop (`quantum/carleman_two_phase_step.py`)**: Classical grid iteration executing local 10-qubit block-encoded Carleman collisions, physical positivity guards, gravitational body forcing, quantum streaming $S$, boundary reflection $B$, and observable moment reconstruction.

---

## 2. Multi-Step Validation Results ($4 \times 4$ Lattice)

```text
============================================================================
MULTI-STEP RESULTS (Freshly Generated from Production Snapshot)
============================================================================

t = 1:
  Density Relative L2 Error:  0.000% (Exact to 5.55e-17 at collision)
  Phase Relative L2 Error:    0.000%
  Total Mass Drift Error:     0.00%
  Postselection P_success:    0.0021
  Dilation Scaling alpha:     58.75

t = 5:
  Density Relative L2 Error:  0.999%
  Phase Relative L2 Error:    14.954%
  Total Mass Drift Error:     0.77%
  Postselection P_success:    0.0002
  Dilation Scaling alpha:     23.58

t = 10:
  Density Relative L2 Error:  0.896%
  Phase Relative L2 Error:    16.546%
  Total Mass Drift Error:     0.86%
  Postselection P_success:    0.0001
  Dilation Scaling alpha:     23.18
============================================================================
```

---

## 3. Hardware & Transpilation Status

* **Target QPU Architecture**: IBM Quantum 127Q Heavy-Hex (`generic_backend_127q`).
* **Logical Circuit**: 10 qubits (9 system qubits $+ 1$ block-encoding ancilla).
* **Transpiled Heavy-Hex Depth**: 76,459 gates.
* **Two-Qubit Gates (CX/ECR)**: 21,133.
* **Transpilation Time**: 1.14 seconds.
* **Dual-Lock Preflight**: **ENGAGED (DRY_RUN PROTECTED)**.
* **Hardware Execution Verdict**: **PREPARED / TRANSPILED; NOT EXECUTED ON REAL QPU.**

---

## 4. Scientific Qualifications

1. **Hybrid Classification**: The solver is a **hybrid quantum-classical algorithm** using local quantum block encoding and classical lattice reconstruction. It is **not** a closed unitary $U^t$ quantum evolution of a global lattice.
2. **Carleman Truncation**: Truncated second-order polynomial collision retains quadratic convective and phase-advective couplings; cubic and higher terms are truncated.
3. **Block Encoding Overhead**: Ancilla postselection success probability $P_{\text{succ}} \sim 10^{-4}$ represents an unmitigated sampling overhead on physical hardware, requiring fault-tolerant Oblivious Amplitude Amplification in asymptotic implementations.
