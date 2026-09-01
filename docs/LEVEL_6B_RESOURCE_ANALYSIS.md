# LEVEL-6B: QUANTUM RESOURCE SCALING & RUNTIME PROFILING

**Document**: Circuit Resource Requirements and Performance Accounting for Level 6B  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Logical Register Breakdown

For a lattice of size $N = N_x \times N_y$:

$$n_{\text{sys}} = \lceil\log_2(N_x N_y)\rceil + 5 + 1 = \log_2 N + 6 \text{ qubits}$$

- Spatial indexing ($|x\rangle \otimes |y\rangle$): $\log_2 N$ qubits.
- Discrete velocity / species index ($|a\rangle$): 5 qubits ($2^5 = 32 \ge 18$).
- Unitary dilation ancilla ($|\text{anc}\rangle$): 1 qubit.

---

## 2. Resource Metrics Across Grid Resolutions

| Mesh Size | Spatial Nodes ($N$) | Logical Qubits ($n_{\text{sys}}$) | Quantum Collision Calls / Step | Transpiled ECR Gates / Block | Classical Memory |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 10 | 16 | 520 | 2.25 KB |
| **$8 \times 8$** | 64 | 12 | 64 | 520 | 9.00 KB |
| **$16 \times 16$** | 256 | 14 | 256 | 520 | 36.00 KB |
| **$32 \times 16$** | 512 | 15 | 512 | 520 | 72.00 KB |
| **$64 \times 32$** | 2,048 | 17 | 2,048 | 520 | 288.00 KB |
| **$128 \times 64$** | 8,192 | **19** | 8,192 | 520 | **1.15 MB** |

---

## 3. Computational Workload & Dilation Success Scaling

- **Dilation Normalization Constant**: $\alpha_C = 7.9004$.
- **One-Step Collision Success Probability**: $p_{\text{succ}} = 1/\alpha_C^2 \approx 1.602 \times 10^{-2}$ ($1.60\%$).
- **Classical Reconstructions per Step**: Exactly 1 hybrid handoff per physical timestep.
