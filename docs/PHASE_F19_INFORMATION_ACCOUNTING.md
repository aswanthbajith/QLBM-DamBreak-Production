# PHASE F19: MULTI-STEP INFORMATION ACCOUNTING
## Memory Scaling and Register Footprint across Multi-Step Horizons

**Document**: Multi-Step Information Accounting Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Information Register Scaling Analysis

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Architecture} & \textbf{Memory Growth / Step} & \textbf{Total Memory @ } T=16 & \textbf{Reversibility Mechanism} \\
\hline
\text{Arch A: Compute-Output} & \mathcal{O}(N_{\text{pop}}) & 4,896 \text{ bits / node} & \text{Retained history chain} \\
\text{Arch B: Environment Dilation} & \mathcal{O}(N_{\text{env}}) & 4,608 \text{ bits / node} & \text{Dissipative reservoir} \\
\text{Arch C: Mode Retention} & \mathbf{\mathcal{O}(1) \ (Constant)} & \mathbf{576 \text{ bits / node}} & \mathbf{\text{Bijective } (f^{\text{eq}}, f^{\text{neq}}) \text{ split}} \\
\hline
\end{array}$$
