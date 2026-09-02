# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Resource Audit & Scalability Analysis (Grid Progressions)

**Document**: Qubit Allocation, Gate Depth, and Scaling Across Grid Resolutions  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Data Logical Qubit Formula

For an $N_x \times N_y$ lattice grid with 9 velocities and 2 phases:
$$n_{\text{data}} = \lceil\log_2 N_x\rceil + \lceil\log_2 N_y\rceil + 4_{\text{vel}} + 1_{\text{phase}} = n_x + n_y + 5$$

$$\begin{array}{|l|c|c|c|c|c|c|c|c|}
\hline
\textbf{Lattice Mesh} & N_x & N_y & \textbf{Nodes } (N) & n_x & n_y & n_{\text{vel}} & n_{\text{phase}} & \textbf{Data Qubits } (n_{\text{data}}) \\
\hline
2 \times 2 \text{ Minimal} & 2 & 2 & 4 & 1 & 1 & 4 & 1 & \mathbf{7 \text{ Logical Qubits}} \\
4 \times 4 \text{ Prototype} & 4 & 4 & 16 & 2 & 2 & 4 & 1 & \mathbf{9 \text{ Logical Qubits}} \\
8 \times 4 \text{ Intermediate} & 8 & 4 & 32 & 3 & 2 & 4 & 1 & \mathbf{10 \text{ Logical Qubits}} \\
16 \times 8 \text{ Coarse Mesh} & 16 & 8 & 128 & 4 & 3 & 4 & 1 & \mathbf{12 \text{ Logical Qubits}} \\
32 \times 16 \text{ Medium Mesh} & 32 & 16 & 512 & 5 & 4 & 4 & 1 & \mathbf{14 \text{ Logical Qubits}} \\
64 \times 32 \text{ Benchmark Mesh} & 64 & 32 & 2,048 & 6 & 5 & 4 & 1 & \mathbf{16 \text{ Logical Qubits}} \\
128 \times 64 \text{ Target Dam-Break} & 128 & 64 & 8,192 & 7 & 6 & 4 & 1 & \mathbf{18 \text{ Logical Qubits}} \\
\hline
\end{array}$$

---

## 2. Gate Complexity Scaling of Reversible Arithmetic Streaming

In gate-level arithmetic streaming, modular increments and decrements for $n$-bit coordinates require:
- **Depth**: $\mathcal{O}(n_x + n_y) = \mathcal{O}(\log(N_x N_y))$ with parallel ripple adders.
- **CX / 2Q Gates**: Scales linearly with the number of coordinate qubits ($n_x + n_y$) rather than exponentially with the lattice node count $N$.
- **Measured Transpiled Heavy-Hex Benchmarks**:
  - $2 \times 2$ Grid (7Q): Transpiled Depth $= \mathbf{604}$, Two-Qubit CX/ECR Gates $= \mathbf{214}$.
  - $4 \times 4$ Grid (9Q): Transpiled Depth $= \mathbf{929}$, Two-Qubit CX/ECR Gates $= \mathbf{362}$.
