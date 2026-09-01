# QUANTUM ADVANTAGE SCOPE & COMPLEXITY BOUNDS FOR CFD

**Date**: 2026-08-19  
**Status**: Authoritative Complexity Specification  

---

## 1. Disproven Claims: Dense Flow-Field Speedup

### 1.1 The Quantum Readout Bottleneck (Holevo Bound)
A persistent fallacy in quantum CFD literature is the claim of "exponential speedup for fluid flow simulation."
While the state vector $|\Psi(t)\rangle$ evolves in a $25$-qubit Hilbert space of dimension $D_C \sim 10.26 \times 10^6$, extracting the complete spatial velocity field $\mathbf{u}(\mathbf{x})$ and phase field $\phi(\mathbf{x})$ on $N$ grid points requires:
$$N_{\text{meas}} = \Omega\left( \frac{N \log N}{\epsilon^2} \right)$$
independent quantum measurements (quantum state tomography).
Because classical LBM performs one time step in $\mathcal{O}(N)$ arithmetic operations, full-field quantum simulation offers **zero quantum speedup** (and in fact suffers huge constant-factor quantum overhead) if dense flow fields are read out.

---

## 2. Surviving Quantum Advantage: Global & Low-Dimensional Observables

Quantum advantage in Lattice Boltzmann CFD is mathematically restricted to **global scalar observables** that can be extracted via **Quantum Amplitude Estimation (QAE)** without full-state tomography.

### 2.1 Quadratic Speedup for Integral Quantities
| Problem / Observable | Classical Complexity | Quantum QAE Complexity | Quantum Advantage |
| :--- | :--- | :--- | :--- |
| **Total Fluid Mass $M$** | $\mathcal{O}(1/\epsilon^2)$ Monte Carlo | $\mathcal{O}(1/\epsilon)$ QAE queries | **Quadratic ($2\times$ exponent)** |
| **Total Kinetic Energy $E_k$** | $\mathcal{O}(1/\epsilon^2)$ Monte Carlo | $\mathcal{O}(1/\epsilon)$ QAE queries | **Quadratic ($2\times$ exponent)** |
| **Integrated Wall Force $F_{\text{wall}}$** | $\mathcal{O}(1/\epsilon^2)$ Monte Carlo | $\mathcal{O}(1/\epsilon)$ QAE queries | **Quadratic ($2\times$ exponent)** |
| **Enstrophy / Circulation** | $\mathcal{O}(1/\epsilon^2)$ Monte Carlo | $\mathcal{O}(1/\epsilon)$ QAE queries | **Quadratic ($2\times$ exponent)** |

### 2.2 Quantum Advantage Classification
* **Dense Field Reconstruction**: **DISPROVEN / FAILED**
* **Global Scalar Amplitude Estimation**: **THEORETICAL ALGORITHMIC OPPORTUNITY**
