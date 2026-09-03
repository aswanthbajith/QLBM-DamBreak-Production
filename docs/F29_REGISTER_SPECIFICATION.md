# PHASE F29: SCALABLE LATTICE QUANTUM REGISTER SPECIFICATION
## Register Layout and Addressing for $N_x \times N_y$ Two-Phase D2Q9 Lattice Boltzmann Networks

**Document**: Scalable Quantum Register Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Register Layout for $4\times 4$ Lattice ($16\text{ Nodes, } 16\text{-bit } Q4.12$)

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Register Category} & \textbf{Word Count} & \textbf{Logical Qubits} & \textbf{Physical Assignment} \\
\hline
\text{System Hydro Populations } |f_i(y, x)\rangle & 16 \times 9 = 144 & 2,304 & 16\text{ nodes } \times 9\text{ directions } \times 16\text{ bits} \\
\text{System Phase Populations } |g_i(y, x)\rangle & 16 \times 9 = 144 & 2,304 & 16\text{ nodes } \times 9\text{ directions } \times 16\text{ bits} \\
\textbf{Subtotal System Registers } (Q_{\text{sys}}) & \mathbf{288\text{ words}} & \mathbf{4,608\text{ qubits}} & \mathbf{Persistent\ Lattice\ State} \\
\hline
\text{Environment Bath } |e_{f,g}(y, x)\rangle & 16 \times 18 = 288 & 4,608 & \text{Stinespring pre-collision bath for each node} \\
\textbf{Subtotal Environment } (Q_{\text{env}}) & \mathbf{288\text{ words}} & \mathbf{4,608\text{ qubits}} & \mathbf{Recycled\ per\ Timestep\ (Open\ System)} \\
\hline
\text{Shared Sequential Workspace} & 3\text{ words} & 48 & \text{Moments, velocity division, CSF, symmetric eq} \\
\textbf{Subtotal Workspace } (Q_{\text{work}}) & \mathbf{3\text{ words}} & \mathbf{48\text{ qubits}} & \mathbf{Shared\ Sequential\ ALU\ Workspace} \\
\hline\hline
\mathbf{Total\ Peak\ 4\times 4\ Lattice\ Qubits} & \multicolumn{2}{c|}{\mathbf{4,608 + 4,608 + 48}} & \mathbf{9,264\ Logical\ Qubits} \\
\hline
\end{array}$$

---

## 2. Register Layout for $8\times 8$ Lattice ($64\text{ Nodes, } 16\text{-bit } Q4.12$)

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Register Category} & \textbf{Word Count} & \textbf{Logical Qubits} & \textbf{Physical Assignment} \\
\hline
\text{System Hydro Populations } |f_i(y, x)\rangle & 64 \times 9 = 576 & 9,216 & 64\text{ nodes } \times 9\text{ directions } \times 16\text{ bits} \\
\text{System Phase Populations } |g_i(y, x)\rangle & 64 \times 9 = 576 & 9,216 & 64\text{ nodes } \times 9\text{ directions } \times 16\text{ bits} \\
\textbf{Subtotal System Registers } (Q_{\text{sys}}) & \mathbf{1,152\text{ words}} & \mathbf{18,432\text{ qubits}} & \mathbf{Persistent\ Lattice\ State} \\
\hline
\text{Environment Bath } |e_{f,g}(y, x)\rangle & 64 \times 18 = 1,152 & 18,432 & \text{Stinespring pre-collision bath for each node} \\
\textbf{Subtotal Environment } (Q_{\text{env}}) & \mathbf{1,152\text{ words}} & \mathbf{18,432\text{ qubits}} & \mathbf{Recycled\ per\ Timestep\ (Open\ System)} \\
\hline
\text{Shared Sequential Workspace} & 3\text{ words} & 48 & \text{Moments, velocity division, CSF, symmetric eq} \\
\textbf{Subtotal Workspace } (Q_{\text{work}}) & \mathbf{3\text{ words}} & \mathbf{48\text{ qubits}} & \mathbf{Shared\ Sequential\ ALU\ Workspace} \\
\hline\hline
\mathbf{Total\ Peak\ 8\times 8\ Lattice\ Qubits} & \multicolumn{2}{c|}{\mathbf{18,432 + 18,432 + 48}} & \mathbf{36,912\ Logical\ Qubits} \\
\hline
\end{array}$$
