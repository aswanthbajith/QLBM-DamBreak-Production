# PHASE F15 FORENSIC GATE AUDIT REPORT
## Strict Mathematical & Code Verification of the Carleman Autonomous Collision

**Document**: Forensic Gate Audit & Rigorous Classification Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Executive Summary & Revised Scientific Classification

$$\mathbf{PHASE\ F15\ SCIENTIFIC\ VERDICT:\ LEVEL\ C}$$

$$\boxed{\text{“COHERENT QUANTUM KERNEL WITH EXPLICIT HYBRID NONLINEAR CONTROL”}}$$

### Critical Forensic Findings:
1. **Level A Classification Formally Revoked**: The previous claim of Level A ("Fully Autonomous Coherent Two-Phase QLBM") is **invalidated and revoked**. The implementation in `f15_autonomous_solver.py` does not execute as an autonomous quantum circuit on QPU hardware; instead, it unpacks statevector amplitudes into Python floats, computes Carleman lifting classically in RAM, applies NumPy collision and streaming, and re-encodes the statevector at every timestep.
2. **Carleman Linearization is Static but Hybrid in Execution**: The $K=2$ Carleman matrix $A_C \in \mathbb{R}^{342 \times 342}$ is genuinely state-independent and static. However, the lifted tensor state $Y_2 = \mathbf{z} \otimes \mathbf{z}$ is not evolved in a physical quantum register; it is classically re-lifted from $\mathbf{z}$ at every timestep.
3. **Sz.-Nagy Dilation Power Leakage Proven**: The block-encoding $U_A$ satisfies $P U_A P = A_C / \alpha_A$ at $K=1$, but suffers from severe dilation leakage for multi-step powers:
   $$\|P U_A^2 P - (A_C/\alpha_A)^2\|_2 = 1.0000 \quad (\text{Relative Error } = 1041.7\%)$$
   $$\|P U_A^{16} P - (A_C/\alpha_A)^{16}\|_2 = 1.0000 \quad (\text{Relative Error } = 8.40 \times 10^9\%)$$
   Applying $U_A^T$ without intermediate projective reset or Oblivious Amplitude Amplification (OAA) is mathematically invalid for multi-step evolution.

---

## 2. Mathematical Derivation of Manifold Truncation

Let $\mathbf{z} \in \mathbb{R}^{18}$ and $Y = [\mathbf{z}; \mathbf{z} \otimes \mathbf{z}] \in \mathbb{R}^{342}$. The Carleman operator is:
$$A_C = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix}$$

Applying $A_C$ to $Y$:
$$Y^* = A_C Y = \begin{bmatrix} M_1 \mathbf{z} + M_2 (\mathbf{z} \otimes \mathbf{z}) \\ (M_1 \otimes M_1)(\mathbf{z} \otimes \mathbf{z}) \end{bmatrix}$$

The true tensor product of the post-collision state $\mathbf{z}^* = M_1 \mathbf{z} + M_2 (\mathbf{z} \otimes \mathbf{z})$ is:
$$\mathbf{z}^* \otimes \mathbf{z}^* = (M_1 \mathbf{z}) \otimes (M_1 \mathbf{z}) + (M_1 \mathbf{z}) \otimes [M_2 (\mathbf{z} \otimes \mathbf{z})] + [M_2 (\mathbf{z} \otimes \mathbf{z})] \otimes (M_1 \mathbf{z}) + [M_2 (\mathbf{z} \otimes \mathbf{z})] \otimes [M_2 (\mathbf{z} \otimes \mathbf{z})]$$

- **Retained Term**: $(M_1 \mathbf{z}) \otimes (M_1 \mathbf{z}) = (M_1 \otimes M_1)(\mathbf{z} \otimes \mathbf{z})$.
- **Discarded Terms**: Cubic cross-terms $\mathcal{O}(\mathbf{z}^3)$ and quartic terms $\mathcal{O}(\mathbf{z}^4)$.
- **Conclusion**: In an autonomous trajectory without re-lifting, $Y_2(t) = (M_1 \otimes M_1)^t Y_2(0)$ receives zero quadratic feedback from $M_2$, causing progressive manifold drift.

---

## 3. Sz.-Nagy Dilation Power Leakage Audit

$$\begin{array}{|c|c|c|c|}
\hline
\textbf{Power } K & \text{Dilation Leakage } \|P U_A^K P - (A_C/\alpha_A)^K\|_2 & \textbf{Relative Error} & \textbf{Verdict} \\
\hline
K = 1 & 0.0000 \times 10^0 & 0.0000 \times 10^0 & \textbf{EXACT (Block Encoding)} \\
K = 2 & 1.0000 \times 10^0 & 1.0417 \times 10^1 & \textbf{LEAKAGE } (P U^2 P \ne A^2) \\
K = 4 & 1.0000 \times 10^0 & 1.7104 \times 10^2 & \textbf{LEAKAGE } (P U^4 P \ne A^4) \\
K = 8 & 1.0000 \times 10^0 & 6.1176 \times 10^4 & \textbf{LEAKAGE } (P U^8 P \ne A^8) \\
K = 16 & 1.0000 \times 10^0 & 8.3986 \times 10^9 & \textbf{LEAKAGE } (P U^{16} P \ne A^{16}) \\
\hline
\end{array}$$

---

## 4. Complete Execution Trace of `f15_autonomous_solver.py`

$$\begin{array}{|c|l|l|c|}
\hline
\textbf{Step} & \textbf{Operation} & \textbf{Execution Mechanism} & \textbf{Classification} \\
\hline
0 & \text{State Initialization} & \text{Initial dam state mapped to } |\Psi_0\rangle & \text{Static Precomputation} \\
1 & \text{Amplitude Extraction} & \text{Loop reads } \psi[\text{idx}] \cdot \mathcal{N} \text{ into NumPy floats} & \textbf{CLASSICAL EXTRACTION} \\
2 & \text{Carleman Lifting} & \mathbf{z}_2 = \mathbf{z} \otimes \mathbf{z} \text{ in Python RAM} & \textbf{CLASSICAL RE-LIFTING} \\
3 & \text{Matrix Collision} & Y^* = A_C Y \text{ via NumPy dot product} & \textbf{CLASSICAL COMPUTATION} \\
4 & \text{Streaming} & \text{NumPy array roll } \texttt{stream(f)} & \textbf{CLASSICAL COMPUTATION} \\
5 & \text{Boundary Bounce-Back} & \text{NumPy array slicing on solid mask} & \textbf{CLASSICAL COMPUTATION} \\
6 & \text{Re-Normalization} & \mathcal{N}_{t+1} = \|\mathbf{f}_{t+1}\|_2, \ \psi = \mathbf{f} / \mathcal{N} & \textbf{STATE RE-ENCODING} \\
7 & \text{Final Readout} & \text{Decode fields at step } T & \text{Final Readout} \\
\hline
\end{array}$$

---

## 5. Summary of What is Genuinely Quantum vs. Hybrid

1. **Genuinely Quantum**:
   - Spatial Arithmetic Streaming $S_{\text{arith}}$: Exact reversible coordinate permutation.
   - Physical Boundary Involution $B_{\text{mask}}$: Exact direction-selective involution ($B^2 = I$).
   - One-step Sz.-Nagy Block-Encoding $U_A$: Exact unitary dilation for $K=1$.
2. **Identified Hybrid Interfaces**:
   - Classical Carleman manifold re-lifting $Y = [\mathbf{z}; \mathbf{z} \otimes \mathbf{z}]$ between timesteps.
   - Classical statevector amplitude extraction and normalization tracking.
   - Dilation leakage preventing repeated unitary power application $(U_A)^T$.
