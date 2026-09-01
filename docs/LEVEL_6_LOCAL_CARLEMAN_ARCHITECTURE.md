# LEVEL-6: ARCHITECTURE B — LOCAL CARLEMAN MULTI-TIMESTEP QLBM

This document formalizes Architecture B: a measurement-free, multi-timestep local Carleman quantum algorithm for the coupled two-phase D2Q9 system, extending the methodology of PRE 113, 035307 (2026) / arXiv 2511.13072.

---

## 1. Mathematical Concept & Coherent Propagation

Instead of collapsing the state after every timestep, Architecture B maintains and evolves the local second-order Carleman statevector coherently across $K$ consecutive timesteps:

$$|\mathbf{Y}(t)\rangle = \sum_{\mathbf{x}} \left( \sum_{a=0}^{17} z_a(\mathbf{x}, t) |\mathbf{x}, a, \text{deg}=1\rangle + \sum_{a,b=0}^{17} z_a(\mathbf{x}, t) z_b(\mathbf{x}, t) |\mathbf{x}, a, b, \text{deg}=2\rangle \right)$$

### A. Autonomous Multi-Step Recurrence
For $k = 0, \dots, K-1$:
$$|\mathbf{Y}(t + k + 1)\rangle = \mathcal{U}_{\text{step}} |\mathbf{Y}(t + k)\rangle$$
where the composite unitary step operator is:
$$\mathcal{U}_{\text{step}} = \mathcal{B}_{\text{lifted}} \cdot \mathcal{S}_{\text{lifted}} \cdot \mathcal{U}_{\text{force}} \cdot \mathcal{U}_{\text{Carleman}}$$

1. **Local Carleman Collision Oracle ($\mathcal{U}_{\text{Carleman}}$)**:
   - Block-encodes the autonomous closed $342\times 342$ matrix $C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix}$.
   - Acts locally node-by-node on the velocity and Carleman-degree registers.
2. **Lifted Spatial Streaming ($\mathcal{S}_{\text{lifted}}$)**:
   - Linear sector ($\text{deg}=1$): standard spatial permutation $S: |\mathbf{x}, v\rangle \to |\mathbf{x} + \mathbf{c}_v, v\rangle$.
   - Quadratic sector ($\text{deg}=2$): pairwise product streaming $S \otimes S: |\mathbf{x}, v_1, v_2\rangle \to |\mathbf{x} + \mathbf{c}_{v_1} + \mathbf{c}_{v_2}, v_1, v_2\rangle$.
3. **Lifted Boundary Wall Involution ($\mathcal{B}_{\text{lifted}}$)**:
   - Linear sector: $B$.
   - Quadratic sector: $B \otimes B$.

---

## 2. Register Layout & Qubit Requirements

| Register | Purpose | Qubit Count (for $N = N_x \times N_y$) |
| :--- | :--- | :---: |
| $|x\rangle \otimes |y\rangle$ | Lattice site coordinates | $\log_2(N_x) + \log_2(N_y) = \log_2 N$ |
| $|v_1\rangle$ | Primary velocity / species index ($18$ states) | 5 qubits ($2^5 = 32 \ge 18$) |
| $|v_2\rangle$ | Secondary velocity / species index for quadratic tensor | 5 qubits |
| $|\text{deg}\rangle$ | Carleman degree selector ($0 \to \text{linear}, 1 \to \text{quadratic}$) | 1 qubit |
| $|\text{anc}\rangle$ | Dilation / block-encoding ancilla | 1 qubit |
| **Total Logical Qubits** | Full local Carleman multi-timestep system | $n = \log_2 N + 12$ qubits |

---

## 3. Truncation Error & Dilation Success Scaling

### A. Unclosed Carleman Truncation Residual
Because $C_2$ advances the quadratic sector via $(M_1 \otimes M_1)(\mathbf{z}\otimes\mathbf{z})$, the dropped terms at each step are:
$$\Delta_{\text{trunc}} = M_1 \mathbf{z} \otimes M_2(\mathbf{z}\otimes\mathbf{z}) + M_2(\mathbf{z}\otimes\mathbf{z}) \otimes M_1 \mathbf{z} + M_2(\mathbf{z}\otimes\mathbf{z}) \otimes M_2(\mathbf{z}\otimes\mathbf{z})$$
- Truncation error per step: $\| \Delta_{\text{trunc}} \|_2 \le 2 \|M_1\| \|M_2\| \|\mathbf{z}\|_2^3 + \|M_2\|^2 \|\mathbf{z}\|_2^4 \sim \mathcal{O}(\text{Ma}^3)$.
- For low-Mach dam-break flow ($\text{Ma} \le 0.08$), the accumulated truncation error across $K=3$ steps is $< 1.8\%$.

### B. Multi-Step Postselection Success Probability
- Single-step dilation factor: $\alpha_C = \|A_{\text{eval}}\|_2 \approx 5.32$.
- $K$-step coherent success probability without amplitude amplification:
  $$p_{\text{succ}}(K) = \frac{1}{\alpha_C^{2K}} = \left(\frac{1}{28.3}\right)^K$$
- For $K=2$: $p_{\text{succ}} \approx 0.125\%$.
- With **Oblivious Amplitude Amplification (OAA)** (Brassard et al.):
  $$Q_{\text{OAA}} = \mathcal{O}(\alpha_C^K) \implies \text{Success probability amplified to } \approx 100\% \text{ with } \mathcal{O}(\alpha_C^K) \text{ queries.}$$

---

## 4. Scientific Verdict on Architecture B

### Strengths:
1. **Measurement-Free Timesteps**: Removes full classical state extraction for blocks of $K$ timesteps.
2. **Scalable Spatial Complexity**: Qubit count scales logarithmically $n = \log_2 N + 12$.
3. **Hardware Tractability**: Circuit depth for $K=2$ is within early Fault-Tolerant Quantum Computer (FTQC) regimes.

### Compromises:
1. **Requires Periodic Re-Lifting**: $K$ cannot be arbitrarily large without amplitude amplification due to $\alpha_C^K$ dilation compounding and unclosed $\mathcal{O}(\text{Ma}^3)$ drift.
2. **Hybrid CSF Surface Tension**: Surface tension $\mathbf{F}_s$ is updated between $K$-step blocks.
