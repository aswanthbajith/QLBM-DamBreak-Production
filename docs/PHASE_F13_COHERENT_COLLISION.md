# PHASE F13: COHERENT COLLISION OPERATOR
## Parameter-Conditioned Unitary Dilation Without Classical Matrix Construction

**Document**: Coherent Collision Dilation Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Sz.-Nagy Block Embedding ($U_C$)

The two-phase collision operator $C(\alpha, \mathbf{u}, \mathbf{F}/\rho) = \text{block\_diag}(M_f, M_g) \in \mathbb{R}^{18 \times 18}$ is embedded into a 6-qubit unitary operator $U_C \in \mathbb{U}(64)$:

$$U_C = \begin{bmatrix} C / \alpha_C & D_* \\ D & -C^\dagger / \alpha_C \end{bmatrix}, \quad D = \sqrt{I - \frac{C^\dagger C}{\alpha_C^2}}, \quad D_* = \sqrt{I - \frac{C C^\dagger}{\alpha_C^2}}$$

- **Dilation Unitarity**: $\|U_C^\dagger U_C - I\|_2 < 1.0 \times 10^{-12}$.
- **Success Probability**: $p_0 = 1 / \alpha_C^2 \approx 0.23 - 0.82$.
- **Projective Postselection**: Success on ancilla state $|00\rangle$.
