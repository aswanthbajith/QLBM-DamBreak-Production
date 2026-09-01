# LEVEL-6 TARGET ARCHITECTURE SPECIFICATION

**Architecture Paradigm**: Local Carleman Multi-Timestep Quantum Two-Phase D2Q9 Solver with Bounded Hybrid Continuum Surface Force (CSF) Feedback  
**Target Execution**: Coherent $K$-timestep quantum block propagation ($K = 2 \dots 4$) with periodic hybrid observable recalibration  
**Application Benchmark**: Martin & Moyce (1952) Experimental Dam-Break Flow  

---

## 1. Mathematical State Representation

For an $N = N_x \times N_y$ lattice grid, the local physical state vector at each lattice site $\mathbf{x}$ is:
$$\mathbf{z}(\mathbf{x}, t) = \begin{bmatrix} f_0(\mathbf{x}, t) \\ \vdots \\ f_8(\mathbf{x}, t) \\ g_0(\mathbf{x}, t) \\ \vdots \\ g_8(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18}$$

The local second-order Carleman lifted state vector is:
$$\mathbf{Y}_{\text{local}}(\mathbf{x}, t) = \begin{bmatrix} \mathbf{z}(\mathbf{x}, t) \\ \mathbf{z}(\mathbf{x}, t) \otimes \mathbf{z}(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18 + 324 = 342}$$

The decoupled global state dimension is:
$$\dim \mathbf{Y}_{\text{decoupled}} = 342 N$$

---

## 2. Quantum Register Architecture

Total logical qubits: $n_{\text{sys}} = \log_2(N_x N_y) + 12$ qubits.

```text
Register Layout:
  |x>      : nqx = ceil(log2(Nx)) qubits (x-coordinate)
  |y>      : nqy = ceil(log2(Ny)) qubits (y-coordinate)
  |v1>     : 5 qubits (primary D2Q9 velocity & species index: 0..8 -> f, 9..17 -> g)
  |v2>     : 5 qubits (secondary D2Q9 velocity & species index for quadratic tensor)
  |deg>    : 1 qubit (Carleman degree selector: |0> -> linear z, |1> -> quadratic z (x) z)
  |anc>    : 1 qubit (Sz.-Nagy unitary dilation / block-encoding ancilla)
```

---

## 3. Quantum Unitary Operators

1. **Local Carleman Collision Oracle ($\mathcal{U}_{\text{Carleman}}$)**:
   $$\mathcal{U}_{\text{Carleman}} = \begin{bmatrix} C_2 / \alpha_C & D_{C_2^*} \\ D_{C_2} & -C_2^\dagger / \alpha_C \end{bmatrix} \in \mathbb{U}(2^{12} = 4096)$$
   where $C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix} \in \mathbb{R}^{342 \times 342}$, $\|C_2\|_2 \approx 5.32$, and $\| \mathcal{U}^\dagger \mathcal{U} - I \|_2 < 10^{-13}$.

2. **Lifted Spatial Streaming Permutation ($\mathcal{S}_{\text{lifted}}$)**:
   - On linear sector ($|\text{deg}=0\rangle$): $|x, y, v_1\rangle \to |(x + c_{x,v_1})\bmod N_x, (y + c_{y,v_1})\bmod N_y, v_1\rangle$.
   - On quadratic sector ($|\text{deg}=1\rangle$): $|x, y, v_1, v_2\rangle \to |(x + c_{x,v_1} + c_{x,v_2})\bmod N_x, (y + c_{y,v_1} + c_{y,v_2})\bmod N_y, v_1, v_2\rangle$.
   - Strictly unitary permutation: $\|\mathcal{S}^\dagger \mathcal{S} - I\|_2 = 0$.

3. **Lifted Boundary Wall Involution ($\mathcal{B}_{\text{lifted}}$)**:
   - On linear sector: $|x_b, y_b, v_1\rangle \to |x_b, y_b, \text{opp}(v_1)\rangle$.
   - On quadratic sector: $|x_b, y_b, v_1, v_2\rangle \to |x_b, y_b, \text{opp}(v_1), \text{opp}(v_2)\rangle$.
   - Strictly unitary orthogonal involution: $\mathcal{B}^\dagger = \mathcal{B}, \mathcal{B}^2 = I$.

---

## 4. Operational $K$-Timestep Execution Cycle

```text
              [ Initial State: f(0), g(0), alpha(0) ]
                               │
                               ▼
              ┌────────────────────────────────────────────────────────┐
              │ 1. Classical Evaluation of CSF Surface Force F_s(t_0)   │
              │    F_s = sigma * kappa(alpha) * grad(alpha)            │
              └───────────────────────────┬────────────────────────────┘
                                          │
                                          ▼
              ┌────────────────────────────────────────────────────────┐
              │ 2. Construct & Encode Lifted State |Y(t_0)>             │
              └───────────────────────────┬────────────────────────────┘
                                          │
                        ┌─────────────────┴─────────────────┐
                        │ FOR k = 0, 1, ..., K-1:           │
                        │   |Y(t + k + 1)> =                │
                        │     B_lifted . S_lifted . U_C |Y> │
                        └─────────────────┬─────────────────┘
                                          │
                                          ▼
              ┌────────────────────────────────────────────────────────┐
              │ 3. Quantum Measurement & Moment Decoding at t_0 + K     │
              │    Extract rho, alpha, u, surge front x*(t), h*(t)     │
              └───────────────────────────┬────────────────────────────┘
                                          │
                                          ▼
              ┌────────────────────────────────────────────────────────┐
              │ 4. Re-calculate F_s and Re-Lift for Next K-Step Block  │
              └────────────────────────────────────────────────────────┘
```

---

## 5. Performance Metrics & Quantitative Acceptance Criteria

1. **Measurement Overhead Reduction**: $K\times$ reduction in quantum-classical handoffs ($K=3 \implies 66.7\%$ fewer measurements).
2. **Surge Front Tracking**: Rel $L_2$ error $< 10\%$ against Martin & Moyce experimental curve on $64\times 32$ mesh.
3. **Mass Conservation**: Liquid volume drift $< 1.5\%$ across 60 timesteps.
4. **Unitary Precision**: $\|\mathcal{U}^\dagger \mathcal{U} - I\|_2 < 10^{-12}$ on all quantum operators.
