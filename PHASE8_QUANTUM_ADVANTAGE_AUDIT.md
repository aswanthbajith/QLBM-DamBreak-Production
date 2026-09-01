# PHASE 8 QUANTUM ADVANTAGE & COMPLEXITY SCOPE AUDIT (STAGE 8.11)

**Status**: Verified Complexity Boundaries & Tomography Readout Limits  
**Date**: 2026-08-19  

---

## 1. Complexity Comparison Breakdown

| Dimension / Task | Classical LBM | Classical Sparse Carleman | Quantum QSVT + QAE (Scalars) | Quantum Full-Field Tomography | Speedup Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Query Complexity** | $\mathcal{O}(N / \epsilon^2)$ | $\mathcal{O}(N / \epsilon^2)$ | $\mathcal{O}(\text{polylog}(N) / \epsilon)$ | $\Omega(N \log N / \epsilon^2)$ | **Quadratic ($2\times$) for Scalars ONLY** |
| **Time / Step Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(d \cdot \alpha \cdot \text{polylog}(N))$ | $\Omega(N \log N / \epsilon^2)$ | **Disproven for Full Field** |
| **Memory / Register Space** | $\mathcal{O}(N)$ words | $\mathcal{O}(N)$ words | $\mathcal{O}(\log N)$ qubits | $\mathcal{O}(\log N)$ qubits | **Logarithmic Qubit Compression** |
| **State Preparation Overhead**| None | None | $\mathcal{O}(\text{polylog}(N))$ | $\mathcal{O}(\text{polylog}(N))$ | **Logarithmic** |
| **Readout / Measurement** | $\mathcal{O}(1)$ direct | $\mathcal{O}(1)$ direct | $\mathcal{O}(1/\epsilon)$ (QAE) | $\Omega(N \log N / \epsilon^2)$ | **Tomography Bottleneck** |

---

## 2. Surviving Theoretical Advantage vs. Disproven Claims
1. **Full-Field Velocity Tomography (DISPROVEN)**: Reconstructing the full $18N$ flow field requires $\Omega(N \log N / \epsilon^2)$ measurements by Holevo's theorem, eliminating any quantum speedup over classical $\mathcal{O}(N)$ LBM.
2. **Global Scalar Integrals (THEORETICAL)**: Extracting global scalars ($M = \int \phi d\mathbf{x}$, $E_k = \frac{1}{2}\int \rho |\mathbf{u}|^2 d\mathbf{x}$, $F_{\text{wall}} = \int p dS$) via Quantum Amplitude Estimation (QAE) achieves an $\mathcal{O}(1/\epsilon)$ query complexity, providing a theoretical quadratic speedup over classical $\mathcal{O}(1/\epsilon^2)$ Monte Carlo.
