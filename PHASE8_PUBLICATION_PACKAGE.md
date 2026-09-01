# PHASE 8 SCIENTIFIC PUBLICATION PACKAGE (STAGE 8.20)

**Project Title**: Rigorous Evaluation and Adversarial Bounds of Quantum Lattice Boltzmann Surrogates for Multiphase Hydrodynamics  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  
**Date**: 2026-08-19  

---

## 1. Publication Executive Package Overview

This package aggregates the complete, auditable research manuscript and supplementary materials ready for journal submission.

### Table of Contents:
1. **Title & Abstract**
2. **Physical Classical Reference Model** (D2Q9 Navier-Stokes + Conservative Allen-Cahn)
3. **Quadratic Mathematical Surrogate** ($p=2$, Constant-Density Regime)
4. **Local Carleman Linearization** ($D_C = 342N$, Bounded Truncation Dynamics)
5. **Unitary Block Encoding** (Canonical CS/Halmos Dilation, Invariant $\alpha = 11.4739$)
6. **QSVT Matrix Inversion** (Odd Chebyshev Transformation, Condition Spectrum $\kappa < 1.5$)
7. **Simulation Lineage & Authenticity** (Hybrid Classical SVD Emulation Disclosure)
8. **Multi-Scale Error Budget** (Shot-Noise SQL Fit, Carleman Truncation Floor)
9. **Quantum Resource Projections** (25 Logical Qubits, 2.97 GB Sparse Storage)
10. **Theoretical Quantum Advantage Scope** (QAE Scalar Advantage vs. Tomography Limits)
11. **Comprehensive Disproven Claims & Limitations**
12. **Clean-Room Reproducibility Pipeline**

---

## 2. Definitive Classification of Findings
* **PROVEN**: $D_C = 342N$, Block encoding unitarity, Invariant $\alpha = 11.4739$, Tomography lower bound $\Omega(N \log N / \epsilon^2)$.
* **VERIFIED / EMPIRICAL**: Classical $\mathcal{O}(N)$ LBM scaling, Martin & Moyce dam-break match, Carleman 200-step error saturation ($\\approx 1.05\\%$), QSVT residual ($5.03 \times 10^{-11}$ at $d=15$).
* **SIMULATED**: Statevector finite-shot sampling, depolarizing noise channel robustness ($\lambda \le 0.05$).
* **EMULATED**: Multi-step dynamical time evolution evaluated via classical CPU SVD functional calculus ($448.8\times$ overhead).
* **THEORETICAL**: Quadratic query speedup for global scalar integrals via QAE; 25-qubit production scaling.
* **DISPROVEN / FAILED**: Variable-density cubic closure ($p=3$), static reciprocal density lifting ($\xi = 1/\rho$), full-field dense quantum speedup.
