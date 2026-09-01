# PHASE 10 QUANTUM HARDWARE LIMITATIONS & NISQ-TO-FTQC BOTTLENECK ANALYSIS (STAGE 10.18)

**Auditor Role**: Lead Quantum Computing Experimentalist & Hardware Analyst  
**Date**: 2026-08-19  

---

## 1. Quantitative Scaling Bottlenecks: Small vs. Full Mesh

| Grid Scale | Nodes ($N$) | Carleman Dim ($D_C$) | Logical Qubits ($n_{\text{tot}}$) | Transpiled CNOT Count | Transpiled Circuit Depth | Physical Qubits Required | NISQ Viability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reduced Primitive (2Q)** | 1 (2 modes) | 2 | 2 | **2** | **12** | 2 | **CLEAN NISQ EXECUTION** |
| **Small Nodal Subsystem (4Q)**| 1 (8 modes) | 8 | 4 | **62** | **114** | 4 | **NOISY NISQ (Fidelity $\approx 0.72$)** |
| **Full Dam Break ($4 \times 2$)**| 8 | 2,736 | 13 | **$\sim 2.5 \times 10^6$** | **$\sim 1.5 \times 10^6$** | $13$ (FTQC: $\approx 3,000$) | **UNEXECUTABLE ON NISQ** |
| **Production ($300 \times 100$)**| 30,000 | 10,260,000 | 25 | **$\sim 2.0 \times 10^8$** | **$\sim 1.0 \times 10^8$** | $25$ (FTQC: $65\text{k}-100\text{k}$) | **FAULT-TOLERANT TARGET ONLY** |

---

## 2. Why Full Dam Break Cannot Run on Current NISQ Hardware
1. **Dense Unitary Decomposition ($O(4^n)$ CNOT Explosion)**: Standard dense CS-dilation of a 13-qubit unitary ($8,192 \times 8,192$) decomposes into $\sim 2.5 \times 10^6$ CNOT gates. With current superconducting 2-qubit error rates ($p_{\text{CX}} \approx 8 \times 10^{-3}$), the overall circuit fidelity is $(1 - 0.008)^{2.5 \times 10^6} \approx 0.000000$.
2. **Missing Sparse LCU Compilation**: To execute on NISQ/early-FTQC hardware, the streaming permutation $S$ and collision tensor $C_2$ must be synthesized as structured Linear Combinations of Unitaries (LCU) rather than generic dense matrices.
3. **State Readout Overhead**: Dense tomography of $18N$ continuous velocity/phase modes requires $\Omega(N \log N / \epsilon^2)$ measurements, creating an insurmountable classical readout bottleneck.
