# PHASE F15: QUANTUM EMBEDDING & BLOCK-ENCODING
## Sz.-Nagy Unitary Dilation ($U_A \in \mathbb{U}(1024)$) and Gate-Level Circuit Architecture

**Document**: Quantum Embedding & Dilation Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Sz.-Nagy Block-Encoding ($U_A$)

$A_C \in \mathbb{R}^{342 \times 342}$ is padded into the 9-qubit Hilbert space $\mathbb{R}^{512 \times 512}$ and embedded into a 10-qubit unitary operator $U_A \in \mathbb{U}(1024)$:

$$U_A = \begin{bmatrix} A_C / \alpha_A & D_* \\ D & -A_C^\dagger / \alpha_A \end{bmatrix}, \quad D = \sqrt{I - \frac{A_C^\dagger A_C}{\alpha_A^2}}, \quad D_* = \sqrt{I - \frac{A_C A_C^\dagger}{\alpha_A^2}}$$

- **Dilation Unitarity**: $\|U_A^\dagger U_A - I\|_2 < 4.08 \times 10^{-14}$.
- **Block Reconstruction**: $\langle 0 | U_A | 0 \rangle = A_C / \alpha_A$.
- **Success Probability**: $p_0 = 1/\alpha_A^2 \approx 0.18 - 0.75$.
