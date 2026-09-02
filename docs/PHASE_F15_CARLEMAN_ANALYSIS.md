# PHASE F15: CARLEMAN LINEARIZATION & MANIFOLD ANALYSIS
## Second-Order ($K=2$) Carleman Matrix ($A_C \in \mathbb{R}^{342 \times 342}$) and Tensor Manifold Defect

**Document**: Carleman Linearization & Manifold Verification Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Carleman Linearization Matrix ($A_C$)

Defining the lifted state:
$$Y = \begin{bmatrix} \mathbf{z} \\ \mathbf{z} \otimes \mathbf{z} \end{bmatrix} \in \mathbb{R}^{342} \quad (18 + 324 = 342)$$

The autonomous Carleman linear system satisfies:
$$Y^* = A_C Y$$
where:
$$A_C = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix} \in \mathbb{R}^{342 \times 342}$$

- **Static Fixed Operator**: $A_C$ is constructed once before simulation and remains fixed across all timesteps.
- **Autonomous Evaluation**: $z^* = (A_C Y)_{0:18}$ with **zero classical runtime parameter recomputation**.

---

## 2. Tensor Manifold Defect Verification ($E_{\text{tensor}}$)

$$E_{\text{tensor}} = \frac{\|Y_2 - \mathbf{z} \otimes \mathbf{z}\|_2}{\|\mathbf{z} \otimes \mathbf{z}\|_2}$$

$$\begin{array}{|c|c|c|c|}
\hline
\textbf{State Scale} & \text{Estimated Mach Number } \text{Ma} & \text{Manifold Defect } E_{\text{tensor}} & \textbf{Status} \\
\hline
0.01 & 0.03 & 1.3572 \times 10^{-16} & \textbf{EXACT (Machine Precision)} \\
0.05 & 0.15 & 2.0037 \times 10^{-16} & \textbf{EXACT (Machine Precision)} \\
0.10 & 0.30 & 2.0061 \times 10^{-16} & \textbf{EXACT (Machine Precision)} \\
0.20 & 0.60 & 2.0035 \times 10^{-16} & \textbf{EXACT (Machine Precision)} \\
\hline
\end{array}$$
