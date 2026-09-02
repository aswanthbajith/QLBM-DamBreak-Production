# PHASE F27: LOCAL QUANTUM REGISTER ARCHITECTURE & SPECIFICATION
## Bit-Level Memory Layout for Two-Phase D2Q9 Lattice Boltzmann Node

**Document**: Local Quantum Register Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Fixed-Point Numeric Format ($Q4.n$)

All continuous physical fields (densities, velocities, forces, curvature, and populations) are discretized into signed two's complement fixed-point integers:
- **Total Bit-Width**: $W = 4 + n$ bits (where $n$ is fractional precision).
  - 1 Sign Bit ($s \in \{0, 1\}$)
  - 3 Integer Bits (range $-8.0 \le X \le +7.999\dots$)
  - $n$ Fractional Bits (LSB resolution $\epsilon = 2^{-n}$)
- **Scaling Factor**: $\text{Scale} = 2^n$.
- **Precision Configurations**:
  - $Q4.8$ ($W=12\text{ bits}$, $\epsilon = 3.906 \times 10^{-3}$)
  - $Q4.12$ ($W=16\text{ bits}$, $\epsilon = 2.441 \times 10^{-4}$)
  - $Q4.16$ ($W=20\text{ bits}$, $\epsilon = 1.526 \times 10^{-5}$)
  - $Q4.20$ ($W=24\text{ bits}$, $\epsilon = 9.537 \times 10^{-7}$)

---

## 2. Complete Local Node Register Allocation ($W=16\text{ bits, } Q4.12$)

$$\begin{array}{|l|c|c|l|l|}
\hline
\textbf{Register Name} & \textbf{Width (Bits)} & \textbf{Total Qubits} & \textbf{Semantic Meaning} & \textbf{Lifecycle Category} \\
\hline
\text{System Hydro Populations } |f_0\dots f_8\rangle & 9 \times 16 & 144 & \text{Hydrodynamic directional populations } f_i & \text{Persistent System State (In/Out)} \\
\text{System Phase Populations } |g_0\dots g_8\rangle & 9 \times 16 & 144 & \text{Phase-field directional populations } g_i & \text{Persistent System State (In/Out)} \\
\hline
\textbf{Subtotal System Registers } (Q_{\text{sys}}) & \mathbf{18 \times 16} & \mathbf{288} & \multicolumn{2}{l|}{\textbf{Persistent Lattice Quantum Memory}} \\
\hline
\text{Environment Preimage Registers } |e_f, e_g\rangle & 18 \times 16 & 288 & \text{Pre-collision microstate for Stinespring dilation} & \text{Open-System Bath (Recycled)} \\
\hline
\textbf{Subtotal Environment } (Q_{\text{env}}) & \mathbf{18 \times 16} & \mathbf{288} & \multicolumn{2}{l|}{\textbf{Recycled per Timestep (Open System)}} \\
\hline
\text{Moment Workspace } |\rho_{\text{work}}, \mathbf{j}\rangle & 3 \times 16 & 48 & \text{Total density } \rho \text{ and momentum } (j_x, j_y) & \text{Temporary (Uncomputed)} \\
\text{Velocity Workspace } |u_x, u_y, u^2\rangle & 3 \times 16 & 48 & \text{Fluid velocity and kinetic energy} & \text{Temporary (Uncomputed)} \\
\text{CSF Stencil Workspace } |\nabla \alpha, \kappa, \mathbf{F}_s\rangle & 3 \times 16 & 48 & \text{Gradients, curvature, and surface force} & \text{Temporary (Uncomputed)} \\
\text{Equilibrium Quadratic Invariants} & 3 \times 16 & 48 & \text{Symmetric diagonal invariants } u_{\text{diag}}^2 & \text{Temporary (Uncomputed)} \\
\text{Positivity Guard Flag Register} & 1 \times 16 & 16 & \text{Comparison indicator for } f_0 \text{ non-negativity} & \text{Temporary (Uncomputed)} \\
\hline
\textbf{Peak Workspace Ancillas } (Q_{\text{work}}) & \mathbf{3 \times 16} & \mathbf{48} & \multicolumn{2}{l|}{\textbf{Sequential Compute-Use-Uncompute-Reuse}} \\
\hline\hline
\mathbf{Total\ Peak\ Logical\ Qubits\ per\ Node} & \multicolumn{2}{c|}{\mathbf{288 + 288 + 48}} & \mathbf{624\ Logical\ Qubits} & \mathbf{Peak\ Node\ Footprint} \\
\hline
\end{array}$$
