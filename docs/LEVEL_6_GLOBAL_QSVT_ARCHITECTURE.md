# LEVEL-6: ARCHITECTURE C — GLOBAL CARLEMAN + QSVT FORMALIZATION

This document formalizes Architecture C: an all-at-once spacetime Quantum Linear System Algorithm (QLSA) solved via Quantum Singular Value Transformation (QSVT) for the coupled two-phase Carleman system.

---

## 1. Global Spacetime Linear System Formulation

For a simulation of $N_t$ timesteps, the multi-timestep evolution is formulated as a single block lower-bidiagonal linear equation:

$$L \mathbf{Y}_{\text{global}} = \mathbf{b}_{\text{global}}$$

$$\begin{bmatrix}
I & 0 & 0 & \dots & 0 \\
-A_C & I & 0 & \dots & 0 \\
0 & -A_C & I & \dots & 0 \\
\vdots & \ddots & \ddots & \ddots & \vdots \\
0 & \dots & 0 & -A_C & I
\end{bmatrix}
\begin{bmatrix}
\mathbf{Y}_0 \\
\mathbf{Y}_1 \\
\mathbf{Y}_2 \\
\vdots \\
\mathbf{Y}_{N_t}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{Y}_{\text{init}} \\
\mathbf{b}_C \\
\mathbf{b}_C \\
\vdots \\
\mathbf{b}_C
\end{bmatrix}$$

where $d_C = 342 N$ is the decoupled local Carleman dimension and $A_C = B \cdot S \cdot A_{\text{eval}}$.

---

## 2. Block-Encoding & QSVT Polynomial Synthesis

1. **Block-Encoding of $L$ ($U_L$)**:
   - $L$ is $(\alpha_L, s, 0)$-block-encoded into a unitary $U_L \in \mathbb{U}(2^{n_{\text{global}}})$:
     $$\langle 0^a| U_L |0^a\rangle = \frac{L}{\alpha_L}, \quad \alpha_L \approx 1 + \|A_C\|_2 \approx 2.92$$
   - Total spacetime qubits: $n_{\text{global}} = \lceil\log_2(N_t + 1)\rceil + \log_2 N + 12$.

2. **Condition Number & Polynomial Degree**:
   - Empirically measured linear scaling:
     $$\kappa(L) \approx 2.5 N_t + 3.0$$
   - For target precision $\epsilon = 10^{-3}$, the QSVT polynomial degree $d_{\text{poly}}$ to approximate $x^{-1}$ over $[-1, -\kappa^{-1}] \cup [\kappa^{-1}, 1]$ is:
     $$d_{\text{poly}} = \mathcal{O}\left( \kappa(L) \ln\left(\frac{1}{\epsilon}\right) \right) \approx 2.5 N_t \ln(1000) \approx 17.27 N_t$$

3. **Global Output State & Final-Time Postselection**:
   - The QSVT circuit outputs the superposition over all spacetime history:
     $$|\mathbf{Y}_{\text{global}}\rangle = \frac{1}{\sqrt{\mathcal{N}}} \sum_{t=0}^{N_t} |t\rangle \otimes |\mathbf{Y}_t\rangle$$
   - To obtain the final dam-break state at $t = N_t$, measure the time register in state $|N_t\rangle$.
   - Postselection success probability:
     $$p(t = N_t) = \frac{\|\mathbf{Y}_{N_t}\|_2^2}{\sum_{t=0}^{N_t} \|\mathbf{Y}_t\|_2^2} \approx \frac{1}{N_t + 1}$$
   - Total queries with Amplitude Amplification on time register:
     $$Q_{\text{total}} = \mathcal{O}\left( \sqrt{N_t} \cdot d_{\text{poly}} \cdot \alpha_L \right) = \mathcal{O}\left( N_t^{1.5} \ln\left(\frac{1}{\epsilon}\right) \right)$$

---

## 3. Scientific Evaluation of Architecture C

### Strengths:
1. **Fully Measurement-Free Spacetime Propagation**: Completely eliminates all intermediate measurements and classical state reinitializations for all $N_t$ steps.
2. **Logarithmic Spatial Qubit Scaling**: Operates in $\mathcal{O}(\log(N_x N_y) + \log N_t)$ qubits.
3. **Provable Asymptotic Speedup for Fixed Time**: Scales $\mathcal{O}(\text{poly}(\log N))$ with mesh resolution.

### Critical Bottlenecks:
1. **Dynamic CSF Surface Tension Incompatibility**: In Architecture C, the entire multi-timestep matrix $L$ must be constant or pre-determined. It cannot accommodate state-dependent non-linear updates to surface tension $\mathbf{F}_s(t) = \sigma \kappa(\alpha_t) \nabla \alpha_t$ without unrolling non-linear tensor networks.
2. **Extreme Circuit Depth**: For $N_t = 100$, QSVT query depth exceeds $10^7$ entangling gates, strictly requiring fault-tolerant logical quantum computers with error-corrected surface codes.
