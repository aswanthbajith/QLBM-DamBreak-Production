# LEVEL-6: ARCHITECTURE A — HYBRID QUANTUM-CLASSICAL (HQC) FORMALIZATION

This document formalizes the operational pipeline, computational complexity, and limitations of the Level-5 Hybrid Quantum-Classical (HQC) baseline architecture.

---

## 1. Operational Flow & Algorithm Pipeline

```text
               ┌────────────────────────────────────────────────────────┐
               │    1. Classical Initialization of f_i, g_i, alpha, rho │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    2. Classical Evaluation of CSF Surface Force F_s    │
               │       F_s(x, y) = sigma * kappa(alpha) * grad(alpha)   │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    3. Local Carleman Collision Evaluation: A_eval Y(z) │
               │       f* = A_eval_f Y(z),  g* = A_eval_g Y(z)          │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    4. Quantum State Encoding: |Psi*> in H_512          │
               │       |Psi*> = sum sqrt(f*/M)|x,y,i,0> + ...           │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    5. Unitary Quantum Streaming: |Psi_str> = S |Psi*>  │
               │       Exact spatial permutation (||S†S - I|| = 0)      │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    6. Unitary Quantum Boundary: |Psi_next> = B |Psi_str│
               │       Exact bounce-back involution (B² = I)            │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    7. Full Quantum Measurement / Classical Decoding    │
               │       Extract f(t+1), g(t+1), rho, alpha               │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    8. Repeat Pipeline for Next Timestep                │
               └────────────────────────────────────────────────────────┘
```

---

## 2. Resource Complexity & Scaling Breakdown

For an $N = N_x \times N_y$ lattice grid evolved over $N_t$ timesteps:

| Resource Metric | Mathematical Expression | $4\times 4$ Mesh ($N=16$) | $32\times 16$ Mesh ($N=512$) | $128\times 64$ Mesh ($N=8192$) |
| :--- | :--- | :---: | :---: | :---: |
| **System Qubits ($n_{\text{sys}}$)** | $\log_2 N + 5$ | 9 qubits | 14 qubits | 18 qubits |
| **Ancilla Qubits** | Fixed block-encoding ancilla | 1 qubit | 1 qubit | 1 qubit |
| **Quantum State Preparations** | $N_t$ amplitude encodings | $N_t$ | $N_t$ | $N_t$ |
| **Quantum Full State Readouts** | $N_t$ tomographic decodings | $N_t$ | $N_t$ | $N_t$ |
| **Classical Floating-Point Ops/Step** | $\mathcal{O}(18 N + 342 N + N_{\text{stencil}})$ | $\approx 6 \times 10^3$ FLOPs | $\approx 2 \times 10^5$ FLOPs | $\approx 3 \times 10^6$ FLOPs |
| **Quantum Gate Depth per Step** | Depth($S$) + Depth($B$) | $\mathcal{O}(\text{poly}(\log N))$ | $\mathcal{O}(\text{poly}(\log N))$ | $\mathcal{O}(\text{poly}(\log N))$ |

---

## 3. Scientific Evaluation of Architecture A

### Strengths:
1. **Full Physical Fidelity**: Exactly incorporates non-local CSF surface tension, phase-dependent viscosity, and boundary conditions without truncation errors from quantum arithmetic.
2. **Strict Stability**: The periodic classical decoding naturally regularizes non-physical statevector drift and enforces exact low-Mach clamping.
3. **Low Qubit Overhead**: Requires only $n = \log_2 N + 5$ qubits (e.g., 18 qubits for $128\times 64$).

### Bottlenecks:
1. **Classical Information Bottleneck**: Requires full quantum state tomography / amplitude extraction $\mathcal{O}(N)$ after *every* single timestep, negating end-to-end quantum speedup across multi-timestep runs.
2. **Measurement Shot Complexity**: Extracting $18N$ amplitudes to precision $\epsilon$ requires $\mathcal{O}(18N / \epsilon^2)$ shots per timestep.
