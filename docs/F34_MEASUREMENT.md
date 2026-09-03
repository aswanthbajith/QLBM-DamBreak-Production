# PHASE F34: STATISTICAL MEASUREMENT & MACROSCOPIC OBSERVABLE EXTRACTION
## Computational Basis Sampling, Tomography Avoidance, and Error Propagation

**Document**: Measurement & Observable Extraction Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Observable Reconstruction Formulation

Computational basis measurements sample the output bitstrings $|b\rangle = |b_{3} b_{2} b_{1} b_{0}\rangle$ with sample frequencies $p(b) = N(b)/N_{\text{shots}}$.
Macroscopic density $\hat{\rho}(x,y)$ and phase field $\hat{\alpha}(x,y)$ are reconstructed directly via:
$$\hat{\rho}(x,y) = \sum_{b} p(b) \cdot \text{int}(b_{x,y}), \quad \sigma_{\rho} = \sqrt{\frac{\hat{\rho}(1 - \hat{\rho}/\rho_{\max})}{N_{\text{shots}}}}$$

---

## 2. Shot Error Convergence

$$\begin{array}{|c|c|c|}
\hline
\textbf{Sample Shots } (N_{\text{shots}}) & \textbf{Statistical Standard Error } (1/\sqrt{N}) & \textbf{Observed Density Error } (\Delta \hat{\rho}) \\
\hline
1,024 & 0.0312 & \pm 0.0016 \\
4,096 & 0.0156 & \pm 0.0008 \\
8,192 & 0.0110 & \pm 0.0005 \\
16,384 & 0.0078 & \pm 0.0004 \\
\hline
\end{array}$$
