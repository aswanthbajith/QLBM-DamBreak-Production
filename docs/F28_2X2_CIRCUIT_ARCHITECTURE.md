# PHASE F28: 2×2 END-TO-END QUANTUM LATTICE CIRCUIT ARCHITECTURE
## Complete System Register Layout, Permutation Network, and Timestep Ordering

**Document**: 2×2 End-to-End Quantum Lattice Circuit Architecture  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. 2×2 Lattice Register Allocation ($16\text{-bit } Q4.12$)

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Register Block} & \textbf{Count (Words)} & \textbf{Logical Qubits} & \textbf{Physical Assignment} \\
\hline
\text{System Hydro Populations } |f_i(y, x)\rangle & 4 \text{ nodes} \times 9 = 36 & 576 & \text{Hydrodynamic populations across 4 nodes } (0,0)\dots (1,1) \\
\text{System Phase Populations } |g_i(y, x)\rangle & 4 \text{ nodes} \times 9 = 36 & 576 & \text{Phase-field populations across 4 nodes } (0,0)\dots (1,1) \\
\textbf{Total System Registers } (Q_{\text{sys}}) & \mathbf{72\text{ words}} & \mathbf{1,152\text{ qubits}} & \mathbf{Persistent\ Lattice\ State} \\
\hline
\text{Environment Dilation } |e_{f,g}(y, x)\rangle & 4 \text{ nodes} \times 18 = 72 & 1,152 & \text{Stinespring pre-collision bath for each node} \\
\textbf{Total Environment Registers } (Q_{\text{env}}) & \mathbf{72\text{ words}} & \mathbf{1,152\text{ qubits}} & \mathbf{Recycled\ per\ Timestep\ (Open\ System)} \\
\hline
\text{Shared Arithmetic Workspace} & 3 \text{ words} & 48 & \text{Sequential scratchpad for moments, velocity, CSF, eq} \\
\textbf{Total Workspace } (Q_{\text{work}}) & \mathbf{3\text{ words}} & \mathbf{48\text{ qubits}} & \mathbf{Shared\ Sequential\ ALU\ Workspace} \\
\hline\hline
\mathbf{Total\ Peak\ 2\times 2\ Lattice\ Qubits} & \multicolumn{2}{c|}{\mathbf{1,152 + 1,152 + 48}} & \mathbf{2,352\ Logical\ Qubits} \\
\hline
\end{array}$$

---

## 2. Validated Level-4 Timestep Execution Chain

$$\begin{array}{rcccl}
\text{Step 1: Local Reversible Collisions} & |X_t\rangle_S \otimes |0\rangle_E &\xrightarrow{\bigotimes V_{(y,x)}}& |X_t^*\rangle_S \otimes |X_t\rangle_E & (\text{Moments} \to \mathbf{u} \to \text{CSF} \to \text{Eq} \to \text{BGK} \to f_0\text{ guard}) \\
\text{Step 2: Spatial Streaming} & |X_t^*\rangle_S &\xrightarrow{\mathcal{U}_{\text{stream}}}& |X_{\text{streamed}}\rangle_S & (\text{Exact coordinate wire permutation } S^\dagger S = I) \\
\text{Step 3: Boundary Bounce-Back} & |X_{\text{streamed}}\rangle_S &\xrightarrow{\mathcal{U}_{\text{boundary}}}& |X_{t+1}\rangle_S & (\text{Exact velocity involution } B^2 = I\text{ on solid walls})
\end{array}$$
