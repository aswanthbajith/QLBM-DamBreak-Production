# PHASE F19: ARCHITECTURE COMPARISON & TRADE-OFF MATRIX
## Comparative Evaluation of Five Candidate Quantum Two-Phase LBM Architectures

---

$$\begin{array}{|l|l|l|l|l|l|}
\hline
\textbf{Criterion} & \textbf{Level-6B Hybrid} & \textbf{Phase F18 Full-Copy} & \textbf{Architecture F19-A} & \textbf{Architecture F19-B} & \textbf{Architecture F19-C} \\
\hline
\textbf{Design Principle} & \text{Local Carleman block} & \text{CNOT fanout to env} & \text{Moment non-eq channel} & \text{Compute-out chain} & \text{Abstract CPTP map} \\
\textbf{Autonomy Status} & \mathbf{HYBRID} & \mathbf{AUTONOMOUS} & \mathbf{AUTONOMOUS\ CPTP} & \mathbf{AUTONOMOUS} & \mathbf{CPTP\ FRAMEWORK} \\
\textbf{Conserved Coherence} & \text{Destroyed (re-encoded)} & \text{Destroyed (0.0000)} & \mathbf{PRESERVED\ (1.0000)} & \text{Preserved in joint reg} & \text{Channel-dependent} \\
\textbf{Degenerate Preimages} & \text{Averaged classically} & \text{Pure equilibrium} & \mathbf{Pure\ equilibrium} & \text{Retained in input reg} & \text{Contracted} \\
\textbf{Environment Scaling} & \text{Constant (1 ancilla)} & \mathcal{O}(T \cdot N_{\text{qubits}})\text{ growth} & \mathbf{Constant\ (Recycled)} & \mathcal{O}(T \cdot N_{\text{qubits}})\text{ growth} & \text{Channel-dependent} \\
\textbf{Two-Phase Fidelity} & < 3.8\%\text{ Martin-Moyce} & \text{Basis exact} & \mathbf{Basis\ exact} & \text{Basis exact} & \text{Density matrix} \\
\textbf{CSF Status} & \text{Full } \sigma > 0 & \sigma = 0\text{ demonstration} & \mathbf{Prospective\ stencil} & \sigma = 0\text{ demonstration} & \text{Abstract} \\
\textbf{Physical Reality} & \text{Physical fluid} & \text{Reversible integer} & \mathbf{Open-system\ channel} & \text{Reversible compute} & \text{Statistical mixture} \\
\hline
\end{array}$$

---

## 1. Architectural Descriptions

### Level-6B Hybrid QLBM:
- **Strengths**: Validated physical dam-break hydrodynamics matching Martin & Moyce (1952) benchmark (<3.8% error); exact mass conservation; permanent frozen baseline.
- **Weaknesses**: Requires classical parameter reconstruction, post-selection, and state re-lifting at each timestep. Not autonomous.

### Phase F18 Full-Copy Reversible Embedding:
- **Strengths**: 100% gate-level reversible arithmetic ($C^{-1} C = I$); autonomous execution between state preparation and readout.
- **Weaknesses**: Copies entire input state to environment ($|x\rangle_S |0\rangle_E \to |F(x)\rangle_S |x\rangle_E$), causing complete computational-basis dephasing ($C(\mathcal{E}(\rho)) = 0$).

### Architecture F19-A (Recommended): Moment-Space Open-System Channel
- **Strengths**: Splits Hilbert space into conserved modes $\mathcal{H}_{\text{cons}}$ and non-equilibrium modes $\mathcal{H}_{\text{neq}}$. Environment registers couple **strictly to non-equilibrium modes**, allowing macroscopic quantum fluid coherence between different velocities/densities to survive 100% intact. Environment qubits can be recycled across timesteps.
- **Weaknesses**: Requires fault-tolerant quantum computing (FTQC) logical registers to implement full fixed-point arithmetic.

### Architecture F19-B: Reversible Compute-Output BGK Embedding
- **Strengths**: Operates strictly via reversible logic $|x_t\rangle |0\rangle \to |x_t\rangle |x_{t+1}\rangle$. Retains all information without dissipation.
- **Weaknesses**: Memory grows linearly with timestep count $T$ ($288 \times (T+1)$ qubits/node). Functions as reversible classical computation rather than an open quantum dissipative physical simulation.

### Architecture F19-C: Quantum Channel QLBM
- **Strengths**: Mathematically rigorous CPTP formalism treating streaming and boundary as channels.
- **Weaknesses**: Lacks circuit compilation details; functions primarily as an analytical framework.
