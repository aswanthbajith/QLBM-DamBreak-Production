# PHASE F16: ROUTE A — HIGHER-ORDER CARLEMAN INVESTIGATION
## Dimension Scaling, Manifold Non-Closure Proof, and Truncation Limits ($K=1 \dots 4$)

**Document**: Higher-Order Carleman Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Carleman Dimension Hierarchy for Two-Phase State ($d_0 = 18$)

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Order } K & \textbf{Lifted Dimension } \dim(Y_K) & \textbf{Qubits / Node} & \textbf{Retained Polynomial Terms} & \textbf{Discarded Cross-Terms} \\
\hline
K = 1 & 18 & 5 & \text{Linear } M_1 \mathbf{z} & \text{All nonlinearities } \mathcal{O}(\mathbf{z}^2) \\
K = 2 & 342 & 9 & M_1 \mathbf{z} + M_2 \mathbf{z}^{\otimes 2} & \text{Cubic } \mathcal{O}(\mathbf{z}^3), \text{ Quartic } \mathcal{O}(\mathbf{z}^4) \\
K = 3 & 6,174 & 13 & \text{Degree } 1 \dots 3 \text{ terms} & \text{Degrees } 4, 5, 6 \\
K = 4 & 111,150 & 17 & \text{Degree } 1 \dots 4 \text{ terms} & \text{Degrees } 5, 6, 7, 8 \\
\hline
\end{array}$$

---

## 2. Mathematical Proof of Infinite Hierarchy & Manifold Non-Closure

For any finite truncation order $K$, applying the linear Carleman matrix $A_C^{(K)}$ yields:
$$Y_K(t) = \left( A_C^{(K)} \right)^t Y_K(0)$$

Because $(z')^{\otimes K}$ generates terms of degree $2K > K$, the tensor manifold condition:
$$E_{\text{tensor}} = \frac{\|Y_K - \mathbf{z}^{\otimes K}\|}{\|\mathbf{z}^{\otimes K}\|}$$
accumulates errors at every timestep unless an explicit non-unitary projection / reset is performed.

$$\mathbf{Conclusion\ on\ Route\ A:\ REJECTED\ as\ an\ autonomous\ architecture.}$$
Carleman linearization cannot close autonomously without infinite Hilbert dimension or classical re-lifting.
