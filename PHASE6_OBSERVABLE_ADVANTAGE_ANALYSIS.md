# PHASE 6 OBSERVABLE ESTIMATION & QUANTUM ADVANTAGE BOUNDS (STAGE 6.9)

**Status**: Verified Quantum Advantage Scope Specification  
**Date**: 2026-08-19  

---

## 1. Observable Complexity Comparison Table

| Observable | Mathematical Definition | Quantum Register Subspace | Classical Complexity | Quantum QAE Complexity | Quantum Advantage | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Liquid Mass ($M$)** | $\int_\Omega \phi(\mathbf{x}) d\mathbf{x}$ | $\sum_q |h_q(\mathbf{x})\rangle$ | $\mathcal{O}(1/\epsilon^2)$ | $\mathcal{O}(1/\epsilon)$ | **Quadratic ($2\times$)** | **THEORETICAL_ADVANTAGE** |
| **Total Kinetic Energy ($E_k$)** | $\frac{1}{2}\int \rho |\mathbf{u}|^2 d\mathbf{x}$ | $|\Psi \otimes \Psi\rangle$ | $\mathcal{O}(1/\epsilon^2)$ | $\mathcal{O}(1/\epsilon)$ | **Quadratic ($2\times$)** | **THEORETICAL_ADVANTAGE** |
| **Wall Impact Force ($F_{\text{wall}}$)** | $\sum_{y} p(x_{\text{wall}}, y)$ | $|g(x_{\text{wall}})\rangle$ | $\mathcal{O}(1/\epsilon^2)$ | $\mathcal{O}(1/\epsilon)$ | **Quadratic ($2\times$)** | **THEORETICAL_ADVANTAGE** |
| **Surge Front Indicator ($x^*$)** | $\max \{ x \mid \phi > 0.5 \} / H$ | $|\phi(x, 0)\rangle$ (Floor) | $\mathcal{O}(N_x/\epsilon^2)$ | $\mathcal{O}(\sqrt{N_x}/\epsilon)$ | **Polynomial** | **THEORETICAL_ADVANTAGE** |
| **Full Velocity Field $\mathbf{u}(\mathbf{x})$** | $\frac{1}{\rho_0}\sum g_q \mathbf{c}_q$ | Complete $|g\rangle$ state | $\mathcal{O}(N)$ | $\Omega(N \log N / \epsilon^2)$ | **NO ADVANTAGE** | **DISPROVEN_SPEEDUP** |

---

## 2. Definitive Quantum Advantage Boundaries
1. **Surviving Advantage**: Restricted to global scalar integrals ($M, E_k, F_{\text{wall}}$) via Quantum Amplitude Estimation (QAE), providing a quadratic $\mathcal{O}(1/\epsilon)$ query reduction.
2. **Disproven Speedup**: Full spatial velocity and phase field reconstruction suffers from the $\mathcal{O}(N)$ tomography bottleneck.
