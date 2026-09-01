# INDEPENDENT REAL IBM QUANTUM HARDWARE EVIDENCE AUDIT

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  

---

## 1. Forensic Audit of Real-Hardware Claims in Literature

| Paper Reference | Claimed Backend | Real QPU Executed? | Execution Evidence | Quantum Circuit | Qubits | Grid Mesh | Timesteps | Real Experimental Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bastida-Zamora et al.** (2026, arXiv:2603.02127) | `ibm_sherbrooke` / `ibm_brisbane` | **YES (Small Hybrid Loop)** | Job IDs & Raw Counts reported for 1D acoustics & 2Q collision | 2Q–4Q Linear OSSLBM Primitive | 2–4 | $1	imes 2$, $1	imes 4$ | 1–2 | **REAL QPU VALIDATED (Small Linear/Hybrid Toy Problem)** |
| **Lăcătuş & Möller** (2025, arXiv:2507.12256) | `ibm_heron` (Native Gate Set) | **NO** | Only transpiled gate counts (724 native gates); no job IDs | 4Q–9Q Surrogate Collision Circuit | 4–9 | N/A (Local node) | 1 (Local) | **TRANSPILED SIMULATION ONLY (No Real QPU Execution)** |
| **Ueno et al.** (2026, arXiv:2606.12770) | None (Generic Transpiler) | **NO** | Statevector simulation data only | 1D Second-Order Carleman QSVT | 6–12 | 1D ($N=4, 8$) | 1 | **CIRCUIT SIMULATION ONLY** |
| **Ueno et al.** (2026, arXiv:2605.28135) | None (Generic Transpiler) | **NO** | Statevector simulation data only | 2D Obstacle Block Encoding | 8–16 | $4	imes 4$, $8	imes 8$ | 1 | **CIRCUIT SIMULATION ONLY** |
| **Nagel & Löwe** (2025, arXiv:2510.05965) | IBM Qiskit Aer | **NO** | Qiskit shot simulation data only | Linear Advection-Diffusion | 4–8 | 1D / 2D small | Multiple | **NOISY SIMULATION ONLY** |
| **Jennings et al. (PsiQuantum)** (2025) | Fault-Tolerant Target | **NO** | Asymptotic complexity proofs | Fault-Tolerant LCU/QSVT | $\sim 10^4$ FTQC | $32	imes 32$ | Multiple | **THEORETICAL FTQC ONLY** |
| **Demirdjian et al.** (2026, arXiv:2605.00302) | None | **NO** | Numerical matrix verification | LCNU $	o$ LCU Data Loading | Analytical | D2Q9 | 1 | **THEORY / NUMERICAL MATRIX ANALYSIS** |
| **Zamora et al. (PR E 113)** (2026) | Qiskit Aer | **NO** | Dynamic circuit statevector simulation | Local Carleman Linearization | $\mathcal{O}(1)$ dynamic | $2	imes 2$, $4	imes 4$ | Multiple | **CIRCUIT SIMULATION ONLY** |

---

## 2. Key Scientific Findings on Hardware Readiness
1. **The Only Genuine Real-QPU Results**: Only Bastida-Zamora et al. (arXiv:2603.02127) have executed tiny 2Q–4Q linear acoustics and localized collision subroutines on physical IBM QPUs.
2. **Surrogate & Carleman Papers**: Papers claiming "IBM Heron compilation" (e.g., Lăcătuş & Möller) performed transpilation benchmarks on simulator topologies, **NOT** physical executions.
3. **Multi-Step Full Dam-Break**: **ZERO** published papers have executed a full multi-step two-phase or free-surface dam-break simulation on a physical quantum computer.
