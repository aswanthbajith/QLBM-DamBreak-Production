# LEVEL-7: THESIS DEFENSE QUESTIONS & ANSWERS (ORAL BRIEFING)
## 27 Essential Defense Questions for Thesis Committee & Academic Examination

**Document**: Oral Examination Defense Preparation Guide  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

### Q1: Why was Carleman linearization needed?
> **Answer**:  
> Standard quantum operators are strictly linear unitaries ($U|\psi\rangle$). The Lattice Boltzmann collision operator contains quadratic convective momentum flux terms ($u_a u_b \sim j_a j_b / \rho$). Carleman linearization maps this nonlinear polynomial dynamical system into an infinite-dimensional linear system that can be truncated and block-encoded into unitary quantum circuits.

---

### Q2: Why second order?
> **Answer**:  
> In Lattice Boltzmann D2Q9 equilibrium expansions, convective momentum flux is quadratic in velocity ($u_a u_b \sim \mathcal{O}(u^2)$). A second-order Carleman truncation ($N_C = 2$) captures the essential kinetic momentum advection and Reynolds stress while keeping the local matrix dimension tractable ($342 \times 342$). Truncation error scales asymptotically as $\mathcal{O}(\text{Ma}^2)$.

---

### Q3: Why does the problem require 342 lifted dimensions?
> **Answer**:  
> The physical state vector $\mathbf{z}(\mathbf{x}) \in \mathbb{R}^{18}$ couples 9 hydrodynamic populations ($f_i$) and 9 phase-field populations ($g_i$). The quadratic Kronecker sector $\mathbf{z} \otimes \mathbf{z}$ has dimension $18 \times 18 = 324$. The total second-order lifted state vector $\mathbf{Y}(\mathbf{x}) = [\mathbf{z}(\mathbf{x}); \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})]$ therefore has dimension $18 + 324 = \mathbf{342}$.

---

### Q4: Why is the unitary dilation larger than the physical Carleman operator?
> **Answer**:  
> To represent the $342 \times 342$ non-unitary Carleman matrix $C_2$ on a quantum computer, it is first padded to the nearest power of two ($512 = 2^9$, requiring 9 system qubits). A Sz.-Nagy unitary dilation embeds a sub-unitary $N \times N$ matrix into a $2N \times 2N$ unitary matrix using 1 additional dilation ancilla qubit ($2 \times 512 = \mathbf{1024 = 2^{10}}$), yielding a 10-qubit unitary operator $U_C \in \mathbb{U}(1024)$.

---

### Q5: What exactly is $\alpha_C$?
> **Answer**:  
> $\alpha_C$ is the sub-unitary dilation normalization factor. To embed a non-unitary matrix $C_2$ into a unitary matrix $U_C = \begin{bmatrix} C_2/\alpha_C & D_* \\ D & -C_2^T/\alpha_C \end{bmatrix}$, the spectral 2-norm of the embedded block must satisfy $\|C_2 / \alpha_C\|_2 \le 1$. We set $\alpha_C = 1.01 \cdot \|C_2\|_2$ to ensure strict sub-unitarity and positive-definiteness of the defect operators $D = \sqrt{I - C_2^T C_2 / \alpha_C^2}$.

---

### Q6: Why does $\alpha_C$ differ between Level 5 and Level 7?
> **Answer**:  
> $\alpha_C$ depends directly on physical kinematic viscosity through the relaxation time $\tau_f = 3\nu + 0.5$. In Level 5 / Level 6A, an exploratory viscosity $\nu = 0.10$ ($\tau_f = 0.80$) gave $\|C_2\|_2 = 7.8222 \implies \alpha_C = \mathbf{7.9004}$. In Level 6B / Level 7, the physical dam-break benchmark parameter $\nu = 0.05$ ($\tau_f = 0.65$) increases the collision frequency $\omega_f = 1/\tau_f = 1.538$, increasing matrix entry magnitudes and yielding $\|C_2\|_2 = 9.6357 \implies \alpha_C = \mathbf{9.7321}$. Both numbers are mathematically exact for their respective physical parameters.

---

### Q7: What caused Level 6A to fail?
> **Answer**:  
> Level 6A attempted autonomous multi-timestep evolution by repeatedly applying $U_C$ and a lifted streaming operator $S_{\text{lifted}}$ on a 342-dimensional state without measurement. It diverged sharply at $K=2$ ($39.9\%$ density error) due to two distinct failure mechanisms: spatial tensor de-correlation under streaming and defect-subspace leakage under dilation powers.

---

### Q8: Why does $S \otimes S$ fail?
> **Answer**:  
> In physical spatial advection, the quadratic entry at node $\mathbf{x}$ is $(\mathbf{z}^* \otimes \mathbf{z}^*)_{ab}(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a) z_b(\mathbf{x} - \mathbf{c}_b)$. When $\mathbf{c}_a \ne \mathbf{c}_b$ (306 out of 324 terms), the two factors originate from *two distinct physical nodes*. Applying a decoupled shift $S \otimes S$ on local node tensors shifts the product by $\mathbf{c}_a + \mathbf{c}_b$ (a single-node shift), which corrupts convective momentum and creates a $\mathbf{419.5\%}$ invariant manifold error on non-uniform fields.

---

### Q9: Why does local re-lifting fix the tensor-manifold problem?
> **Answer**:  
> By restricting spatial streaming strictly to the 18 linear populations ($\mathcal{S}\mathbf{z}$), each discrete velocity population $z_a$ shifts independently to its correct destination node. Local quadratic re-formation $(\mathbf{z} \otimes \mathbf{z})(\mathbf{x})$ at each node after streaming reconstructs the exact local quadratic tensor from the properly arrived populations, preserving $Y_2 = \mathbf{z} \otimes \mathbf{z}$ to machine precision ($0.000000 \times 10^0$).

---

### Q10: Why does repeated unitary dilation leak?
> **Answer**:  
> For any non-unitary operator, the dilation defect block $D_* D = I - C_2 C_2^T / \alpha_C^2 \ne 0$. Multiplying unprojected unitary dilations mixes the dilation complement subspace back into the physical block: $P (\alpha_C U_C)^2 P^T = C_2^2 + \alpha_C^2 D_* D \ne C_2^2$. This causes an unprojected leakage error of $\mathbf{2098.7\%}$ at $K=2$ and $\mathbf{155830\%}$ at $K=4$.

---

### Q11: Why does projection/reset fix the leakage?
> **Answer**:  
> Performing a mid-circuit projective measurement and reset onto $|0_{\text{anc}}\rangle$ after each collision block projects the state vector back onto the physical subspace, setting the defect amplitude to zero. This reproduces the finite-dimensional operator power $[P (\alpha_C U_C) P^T]^K = C_2^K$ to numerical precision ($< 1.71 \times 10^{-15}$ across $K \le 32$).

---

### Q12: Is Level 7 fully coherent?
> **Answer**:  
> No. Because mid-circuit projective measurement and ancilla reset collapse quantum superposition between the physical register and the ancilla at every timestep, the evolution is not continuous uninterrupted coherence. It is classified as **projected multi-step block-encoded quantum evolution with intermediate ancilla resets**.

---

### Q13: Is Level 7 measurement-free?
> **Answer**:  
> No. Intermediate projective ancilla resets and classical moment decoding are mathematically mandatory to eliminate defect-subspace leakage and evaluate non-local forces.

---

### Q14: Is Level 7 fully quantum?
> **Answer**:  
> No. It is a **Hybrid Quantum-Classical (HQC)** architecture. Local collision and linear streaming are quantum-encoded, while non-local Continuum Surface Force (CSF) curvature stencils and moment decoding are evaluated on classical CPU.

---

### Q15: Why is CSF classical?
> **Answer**:  
> Brackbill surface tension $\mathbf{F}_s = \sigma \kappa \nabla\alpha$ requires computing interface normal vectors $\mathbf{n} = \nabla\alpha / |\nabla\alpha|$ and spatial curvature $\kappa = -\nabla\cdot\mathbf{n}$. An autonomous quantum arithmetic circuit for non-local spatial stencils, division, and square roots would require $> 50,000$ Toffoli gates per node. Evaluating CSF classically in a hybrid feedback loop preserves physical accuracy without intractable quantum overhead.

---

### Q16: What does OAA actually improve?
> **Answer**:  
> Oblivious Amplitude Amplification (OAA) boosts the one-step postselection success probability of the block-encoded collision from $p_0 = 1/\alpha_C^2 \approx 1.056\%$ up to **$99.928\%$ per amplified block** using $m=7$ Grover iterations.

---

### Q17: Is 99.93% the probability of the whole simulation?
> **Answer**:  
> No. $99.93\%$ is the success probability of a single amplified collision block. For a multi-step simulation of $K$ consecutive blocks, the cumulative success probability compounds as $p_{\text{total}}(K) = (p_{\text{step}})^K$ (e.g., $(0.999283)^{32} = \mathbf{97.73\%}$ for $K=32$ blocks).

---

### Q18: How many logical qubits are required?
> **Answer**:  
> For a $128 \times 64$ lattice ($8,192$ nodes), the architecture requires **19 data logical qubits** and **2 algorithmic ancillas**, giving a complete register allocation of **21 logical qubits**.

---

### Q19: Why 19 versus 21?
> **Answer**:  
> 19 qubits represents the **principal data encoding registers** ($7_x + 6_y + 5_{\text{vel}} + 1_{\text{dilation\_anc}}$). 21 qubits represents the **complete algorithmic configuration**, adding 1 phase/reflection ancilla for OAA and 1 ripple-carry work qubit for reversible spatial streaming adders.

---

### Q20: Can this run on an IBM QPU?
> **Answer**:  
> No. Transpilation of a single local 10-qubit collision block onto IBM FakeSherbrooke (127Q Heavy-Hex) yields a circuit depth of $\approx \mathbf{3.76\text{M}}$ and $\approx \mathbf{831\text{k}}$ two-qubit ECR gates. In the presence of physical NISQ noise, the circuit fidelity is effectively zero.

---

### Q21: Why is it not NISQ practical?
> **Answer**:  
> Under a simplified independent-error model with state-of-the-art two-qubit gate fidelity ($99.7\%$), the survival probability across $831,000$ entangling gates would be $(0.997)^{831,000} \approx 10^{-1084}$, yielding pure white noise. The demonstrated resource scale places the algorithm strictly in the **Fault-Tolerant Quantum Computing (FTQC)** regime.

---

### Q22: Does this demonstrate quantum speedup?
> **Answer**:  
> No. Emulation on classical CPUs scales exponentially in qubit count, and physical quantum speedup requires fault-tolerant logical QPUs with low error-correction overhead.

---

### Q23: Does this demonstrate quantum advantage?
> **Answer**:  
> No. Quantum advantage has not been demonstrated and remains an open research problem.

---

### Q24: What is actually novel?
> **Answer**:  
> Candidate contributions include: (1) First formal derivation of the spatial tensor streaming obstruction in discrete velocity kinetic lattices; (2) First coupled 18-variable hydrodynamic-phase Carleman block encoding; (3) Systematic derivation of dilation leakage and projective reset composition; and (4) First physical comparison of a Carleman QLBM against experimental dam-break benchmarks (Martin & Moyce 1952).

---

### Q25: What remains unsolved?
> **Answer**:  
> Open problems include: (1) Autonomous on-chip quantum arithmetic compilation for curvature stencils; (2) Fully fault-tolerant surface-code compilation and error-correction overhead analysis; and (3) Third-order Carleman truncation ($\mathcal{O}(\text{Ma}^3)$) for higher Reynolds number regimes.

---

### Q26: Why is Level 6B still important?
> **Answer**:  
> Level 6B is the frozen, validated physical baseline. It provides the validated classical-quantum comparison benchmark with bounded mass drift ($\le 1.53\%$) and proven dam-break hydrodynamics, serving as the ground truth for all quantum operator analyses.

---

### Q27: What is the strongest defensible thesis contribution?
> **Answer**:  
> Developing a validated coupled two-phase Carleman block-encoded Lattice Boltzmann representation, systematically discovering and diagnosing the mathematical failure modes of multi-step lifted propagation (streaming de-correlation and dilation leakage), and proving that linear permutation streaming with mid-circuit projective resets resolves both failure modes to machine precision.
