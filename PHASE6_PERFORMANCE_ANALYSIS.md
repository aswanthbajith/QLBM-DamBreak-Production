# PHASE 6 CLASSICAL VS HYBRID QUANTUM PERFORMANCE ANALYSIS (STAGE 6.8)

**Status**: Verified Performance Benchmarking on $4 \times 2$ Grid (20 Steps)  
**Date**: 2026-08-19  

---

## 1. Runtime & Memory Comparison Table

| Method / Solver | Total Time (s) | Step Time (ms) | Peak RAM (MB) | Surge Front $x^*$ | Linear Residual | State Fidelity | Overhead Factor | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Classical Direct LBM** | 0.163 | 8.14 | 0.03 | 1.00 | $0.0$ | 1.0000 | **$1.0\times$ (Baseline)** | **MEASURED** |
| **Carleman Linear Solver** | 0.163 | 8.15 | 15.69 | 1.00 | $0.0$ | 0.9455 | **$1.0\times$** | **MEASURED** |
| **Hybrid QSVT Emulation** | 73.062 | 3653.08 | 3090.65 | 1.00 | $9.07 \times 10^{-11}$ | 0.9455 | **$448.8\times$** | **HYBRID EMULATION** |

---

## 2. Critical Performance Takeaways
1. **Classical Emulation Overhead**:
   Evaluating the QSVT pipeline via classical CPU SVD functional calculus incurs a **$448.8\times$ slowdown** and substantial memory overhead relative to direct classical LBM.
2. **No Classical Speedup**:
   This confirms rule 8: the hybrid SVD implementation is an emulation tool for validating quantum algorithm correctness, **not** a faster classical solver.
3. **Physical Equivalence**:
   Both the Carleman solver and QSVT emulator reproduce the exact surge front position $x^* = 1.00$ matching classical CFD.
