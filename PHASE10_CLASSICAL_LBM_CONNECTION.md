# PHASE 10 CLASSICAL CFD TO QUANTUM HARDWARE CONNECTION MATRIX (STAGE 10.16)

**Status**: Verified Algorithmic Traceability  
**Date**: 2026-08-19  

---

## 1. Direct Traceability Matrix

| Classical Dam-Break Component | Mathematical Quantum Representation | Quantum Circuit Object | Hardware Experiment | Measured Quantity | Implementation Lineage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **D2Q9 Populations ($g_q, h_q$)** | State Vector $\Psi \in \mathbb{R}^{18N}$ | `Small_QLBM_State` (4Q) | `04_small_qlbm_state.py` | State amplitudes $\langle i|\Psi\rangle$ | **CLASSICAL $\to$ SIMULATED** |
| **BGK / Allen-Cahn Collision** | Quadratic Map $M_1 \Psi + M_2 (\Psi \otimes \Psi)$ | `Block_Enc_2Q` (2Q) | `01_block_encoding_demo.py` | Unitary element $\langle 0|U_A|0\rangle$ | **CLASSICAL $\to$ HARDWARE PRIMITIVE** |
| **Streaming Shift Operator ($S$)** | Permutation Matrix $S \in \{0, 1\}^{18N \times 18N}$ | Sparse permutation logic | Integrated in $A_C$ builder | Shifted basis modes | **CLASSICAL CPU** |
| **Carleman Lifting** | Mode Expansion $Y = [\Psi; \Psi \otimes \Psi] \in \mathbb{R}^{342N}$ | Dimension $D_C = 342N$ | Analytical structure | Lifted state vector | **CLASSICAL NUMERICAL** |
| **Unitary Block Encoding** | Canonical Dilation $U_A \in \mathbb{C}^{2d \times 2d}$ | `U_A` in Qiskit | `01_block_encoding_demo.py` | Dilated unitary blocks | **CLASSICAL DILATION / HARDWARE PRIMITIVE** |
| **QSVT Matrix Inversion** | Odd Chebyshev $P(x) \approx 1/(\alpha x)$ | `QSVT_2Q_deg3` (2Q) | `02_qsvt_demo.py` | Inverted state $M^{-1}|b\rangle$ | **HARDWARE PRIMITIVE (2Q) / SVD EMULATION (Multi-step)** |
| **Time Evolution ($t=1..200$)** | Iterated Inversion $Y(t+1) = M^{-1} Y(t)$ | Classical loop over SVD | `dam_break_qlbm_sim.py` | State trajectory $Y(t)$ | **CLASSICAL CPU SVD EMULATION** |
| **Macroscopic Mass ($M$)** | Order Parameter Integral $\int \phi d\mathbf{x}$ | `QAE_Mass_Scalar` (3Q) | `05_qae_scalar_demo.py` | Target subspace amplitude | **HARDWARE PRIMITIVE / QAE BLUEPRINT** |
