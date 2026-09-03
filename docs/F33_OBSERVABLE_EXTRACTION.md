# PHASE F33: OBSERVABLE EXTRACTION & SHOT CONVERGENCE
## Statistical Reconstruction of Hydrodynamic Densities, Phase Fields, and Standard Errors

**Document**: Observable Extraction Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Macroscopic Observable Estimation

Computational basis measurement produces a sampled frequency distribution $p(x) = \frac{N(x)}{N_{\text{shots}}}$ over $16$-bit bitstrings.
Macroscopic density $\hat{\rho}(x,y)$ and phase field $\hat{\alpha}(x,y)$ are reconstructed via expectation values:
$$\hat{\rho}(x,y) = \sum_{b} p(b) \cdot \text{int}(b_{x,y}), \quad \sigma_\rho = \sqrt{\frac{\hat{\rho}(1 - \hat{\rho}/\rho_{\max})}{N_{\text{shots}}}}$$

---

## 2. Shot Scaling Convergence

$$\begin{array}{|c|c|c|}
\hline
\textbf{Shots } (N_{\text{shots}}) & \textbf{Theoretical Standard Error } (1/\sqrt{N}) & \textbf{Density Uncertainty } (\Delta \hat{\rho}) \\
\hline
100 & 0.1000 & \pm 0.0050 \\
500 & 0.0447 & \pm 0.0022 \\
1,000 & 0.0316 & \pm 0.0016 \\
5,000 & 0.0141 & \pm 0.0007 \\
10,000 & 0.0100 & \pm 0.0005 \\
\hline
\end{array}$$
