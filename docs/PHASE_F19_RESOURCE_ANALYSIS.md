# PHASE F19: QUANTUM RESOURCE AND SCALING ANALYSIS
## Exact Qubit Allocations, Gate Complexity, and Multi-Step Memory Scaling

---

## 1. Per-Node Register Resource Allocations

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Architecture} & \textbf{Data Qubits} & \textbf{Env Qubits} & \textbf{Work Qubits} & \textbf{Total Qubits/Node} & \textbf{Toffolis/Node/Step} \\
\hline
\text{NISQ Demonstrator (2x2)} & 4 & 0 & 0 & \mathbf{4} & 0\text{ (16 ECR total)} \\
\text{FTQC Baseline (F29)} & 288 & 288 & 48 & \mathbf{624} & 21,168 \\
\text{FTQC Reduced (F31)} & 288 & 224 & 48 & \mathbf{560} & 15,232 \\
\mathbf{Moment\ Channel\ (F19-A)} & 288 & 48 & 48 & \mathbf{384} & \mathbf{7,616} \\
\text{Compute-Output (F19-B)} & 288 & 288 \times T & 48 & \mathbf{288(T+1) + 48} & 15,232 \\
\hline
\end{array}$$

### Optimization Highlight in Architecture F19-A:
By restricting the environment to non-equilibrium modes only, the required environment qubits drop from 224 qubits/node to **48 qubits/node** (a **$78.6\%$ reduction** in environment registers), and the Toffoli gate count drops from 15,232 to **7,616** per node per timestep (a **$50.0\%$ reduction**).

---

## 2. Lattice Mesh Resource Scaling for Architecture F19-A

$$\begin{array}{|l|c|c|c|c|l|}
\hline
\textbf{Mesh Size} & \textbf{Total Nodes} & \textbf{Logical Qubits} & \textbf{Toffoli Count/Step} & \textbf{T-Gate Count/Step} & \textbf{Execution Tier} \\
\hline
2 \times 2 & 4 & 1,536 & 30,464 & 121,856 & \text{Simulated at Gate Level} \\
4 \times 4 & 16 & 6,144 & 121,856 & 487,424 & \text{Simulated at Gate Level} \\
8 \times 8 & 64 & 24,576 & 487,424 & 1,949,696 & \text{Analytical Synthesis} \\
16 \times 16 & 256 & 98,304 & 1,949,696 & 7,798,784 & \text{Analytical Synthesis} \\
128 \times 64 & 8,192 & 3,145,728 & 62,390,272 & 249,561,088 & \text{Industrial FTQC Extrapolation} \\
\hline
\end{array}$$

---

## 3. Multi-Step Environment Scaling vs. Timesteps ($T$)

$$\begin{array}{|c|c|c|c|l|}
\hline
\textbf{Timesteps } T & \textbf{F18 (No Reset)} & \textbf{F19-B (Compute-Out)} & \mathbf{F19-A\ (Dissipative\ Reset)} & \textbf{Physical Viability} \\
\hline
T = 1 & 288\text{ qubits} & 576\text{ qubits} & \mathbf{48\ qubits} & \text{Executable on FTQC} \\
T = 4 & 1,152\text{ qubits} & 1,440\text{ qubits} & \mathbf{48\ qubits} & \text{Executable on FTQC} \\
T = 16 & 4,608\text{ qubits} & 4,896\text{ qubits} & \mathbf{48\ qubits} & \text{Executable on FTQC} \\
T = 64 & 18,432\text{ qubits} & 18,720\text{ qubits} & \mathbf{48\ qubits} & \mathbf{Constant\ in\ T\ (Recycled)} \\
\hline
\end{array}$$

### Critical Scaling Result:
While un-reset full-copying environments scale linearly with time ($\mathcal{O}(T)$ qubit explosion), Architecture F19-A with dissipative reset recycles the 48 non-equilibrium environment ancillas at every timestep, achieving **$\mathcal{O}(1)$ constant qubit scaling in time**.
