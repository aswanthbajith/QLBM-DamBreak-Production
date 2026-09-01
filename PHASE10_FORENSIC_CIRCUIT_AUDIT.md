# PHASE 10 FORENSIC AUDIT OF PRIMARY HARDWARE EXPERIMENTS (STAGE 10.2)

**Auditor Role**: Lead Quantum Algorithm Engineer & Experimentalist  
**Date**: 2026-08-19  

---

## 1. Deep Forensic Evaluation of Hardware Demonstrations

### Experiment 1: `01_block_encoding_demo.py`
1. **Mathematical Operation**: Canonical Halmos CS-dilation of a $2\times 2$ matrix $A = \begin{pmatrix} 0.85 & 0.15 \\ 0.10 & 0.75 \end{pmatrix}$ representing a local two-phase LBM relaxation sub-block.
2. **Prepared State**: $|0\rangle_{\text{sys}} \otimes |0\rangle_{\text{ancilla}}$.
3. **Intended Observable**: Top-left block matrix elements $\langle 0_{\text{anc}}| U_A | 0_{\text{anc}} \rangle = A / \alpha$.
4. **Ideal Result**: Unitarity error $< 3 \times 10^{-16}$, block extraction error $\equiv 0.0$.
5. **Measurement Mechanism**: Projective measurement on dilation ancilla ($q_1$) to verify subspace containment.
6. **Connection to Classical LBM**: Direct local collision relaxation step for 2 discrete distribution modes.
7. **Pipeline Representation**: **Class B — Reduced QLBM Demonstration**.

### Experiment 2: `02_qsvt_demo.py`
1. **Mathematical Operation**: Single-step QSVT matrix inversion $P(A/\alpha) \approx (I + 0.01 A)^{-1}$ using odd Chebyshev polynomial ($d=3, 5$).
2. **Prepared State**: System register in $|0\rangle$, ancilla in $|0\rangle$, subjected to alternating phase rotations $R_z(2\phi_j)$.
3. **Intended Observable**: Inverted state $|\psi_{\text{sol}}\rangle = M^{-1} |b\rangle$.
4. **Ideal Result**: Linear residual $\le 9.60 \times 10^{-4}$ ($d=3$), state fidelity $F = 0.999999$.
5. **Measurement Mechanism**: Statevector tomography / computational basis sampling.
6. **Connection to Classical LBM**: Linear implicit time step $(I + \Delta t A_C)^{-1} Y(t)$.
7. **Pipeline Representation**: **Class B — Reduced QLBM Demonstration**.

### Experiment 3: `03_measurement_demo.py`
1. **Mathematical Operation**: Bell state synthesis followed by computational basis readout on 2 qubits.
2. **Prepared State**: $\frac{1}{\sqrt{2}}(|00\rangle + e^{0.5i}|11\rangle)$.
3. **Intended Observable**: Probability distribution $P(00) = 0.5, P(11) = 0.5$.
4. **Ideal Result**: Zero population in $|01\rangle$ and $|10\rangle$.
5. **Measurement Mechanism**: Direct measurement into classical registers `c[0]`, `c[1]`.
6. **Connection to Classical LBM**: Generic quantum measurement infrastructure and ancilla readout.
7. **Pipeline Representation**: **Class C — Generic Quantum Infrastructure Demonstration**.

### Experiment 4: `05_qae_scalar_demo.py`
1. **Mathematical Operation**: Grover reflection oracle $\mathcal{S}_0 = I - 2|0\rangle\langle 0|$ on target subspace marked by liquid density.
2. **Prepared State**: Uniform superposition $|+\rangle^{\otimes 3}$ across 2 system qubits and 1 QAE ancilla.
3. **Intended Observable**: Target state amplitude representing total liquid mass scalar $M = \int \phi d\mathbf{x}$.
4. **Ideal Result**: Constructive interference on marked computational basis states.
5. **Measurement Mechanism**: Ancilla register measurement `c[0]`.
6. **Connection to Classical LBM**: Global liquid mass integral extraction via QAE query speedup.
7. **Pipeline Representation**: **Class B — Reduced QLBM Demonstration (QAE Reflection Oracle)**.

---

## 2. Summary Classification

| Script | Exact Classification | Scientific Justification |
| :--- | :--- | :--- |
| `01_block_encoding_demo.py` | **Class B (Reduced QLBM Primitive)** | Faithfully encodes local 2-phase LBM collision tensor into unitary subspace. |
| `02_qsvt_demo.py` | **Class B (Reduced QLBM Primitive)** | Implements actual QSVT alternating phase sequence for linear inversion. |
| `03_measurement_demo.py` | **Class C (Quantum Infrastructure)** | Verifies classical register binding and measurement readout fidelity. |
| `05_qae_scalar_demo.py` | **Class B (Reduced QLBM Primitive)** | Demonstrates Grover reflection oracle for macroscopic fluid mass scalar. |
