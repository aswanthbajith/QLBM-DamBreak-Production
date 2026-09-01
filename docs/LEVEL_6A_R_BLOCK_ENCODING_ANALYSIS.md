# LEVEL-6A-R: REPEATED BLOCK-ENCODING & DILATION LEAKAGE ANALYSIS

**Document**: Mathematical Analysis of Unitary Dilations, Subspace Leakage, and Repeated Time Evolution  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Unitary Block-Encoding Formalism

Let $A \in \mathbb{R}^{d \times d}$ be a non-unitary linear operator with sub-unitary scaling $A/\alpha$ ($\|A\|_2 \le \alpha$).
A unitary dilation $U \in \mathbb{U}(2d)$ block-encodes $A/\alpha$ in the top-left block:

$$U = \begin{bmatrix} A/\alpha & D_* \\ D & -A^T/\alpha \end{bmatrix}$$

where $D = \sqrt{I - A^T A / \alpha^2}$ and $D_* = \sqrt{I - A A^T / \alpha^2}$ are the Sz.-Nagy defect operators.
Let $P = [I_d, 0_{d \times d}]$ be the projection onto the primary physical subspace (ancilla state $|0\rangle$).

---

## 2. Repeated Unprojected Dilation Multiplication

Applying the unprojected unitary operator $U$ repeatedly for $K$ steps yields:

$$P (\alpha U) P^T = A$$

$$P (\alpha U)^2 P^T = P \alpha^2 \begin{bmatrix} A^2/\alpha^2 + D_* D & \dots \\ \dots & \dots \end{bmatrix} P^T = A^2 + \alpha^2 D_* D$$

In general, for any non-unitary operator $A$ where $\|A\|_2 < \alpha$, the defect product $D_* D = I - A A^T / \alpha^2 \ne 0$.
Therefore:

$$P (\alpha U)^K P^T = A^K + \mathcal{E}_{\text{leakage}}(K)$$

where the leakage operator $\mathcal{E}_{\text{leakage}}(K)$ grows rapidly with $K$.

### Exact Numerical Measurement on Carleman Matrix $C_2 \in \mathbb{R}^{342 \times 342}$:
- $\alpha_C = 7.9004$
- **Unprojected Multi-Step Error** $\|P (\alpha_C U_C)^K P^T - C_2^K\| / \|C_2^K\|$:
  - $K = 1$: $1.37 \times 10^{-17}$ (Exact)
  - $K = 2$: $10.60$ (**$1059.9\%$ Error**)
  - $K = 3$: $76.72$ (**$7671.6\%$ Error**)
  - $K = 4$: $623.51$ (**$62351.0\%$ Error**)

---

## 3. Evaluation of Candidate Preservation Mechanisms

| Mechanism | Description | Mathematical Precision | Ancilla Overhead | Measurement Overhead | Success Probability |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Unprojected Dilation ($U_C^K$)** | Naive unitary chain without resets | **FAILS ($> 1000\%$ error)** | 1 ancilla | 0 measurements | $\alpha_C^{-2K}$ |
| **2. Projective Measurement / Reset** | Project ancilla onto $|0\rangle$ after each step | **Machine precision ($< 10^{-16}$)** | 1 ancilla | 1 projective reset/step | $\alpha_C^{-2K}$ |
| **3. Oblivious Amplitude Amplification** | $\mathcal{O}(\alpha_C)$ Grover reflections per step | High | +1 ancilla | Projective verification | $\approx 100\%$ |
| **4. Spacetime QSVT ($L \mathbf{y} = \mathbf{b}$)** | Polynomial inversion of spacetime matrix $L$ | Controlled $\epsilon$-precision | Phase ancillas | Readout at $t=N_t$ | $\mathcal{O}(1/N_t)$ |
| **5. Hybrid $K=1$ Classical Re-lifting** | Local Carleman collision + classical re-lifting | **Exact ($0.023\%$ physical error)** | 1 ancilla | 1 readout/step | **$100\%$ (Classically normalized)** |

---

## 4. Key Conclusion on Quantum Embeddings

> [!IMPORTANT]
> **Definitive Scientific Finding**: A one-step unitary dilation $U$ **CANNOT** be multiplied repeatedly in an unprojected quantum circuit to compute $(C_2)^K$.
> Any valid multi-step quantum implementation of a non-unitary Carleman map **MUST** incorporate either:
> 1. Mid-circuit projective measurement / reset after each step, OR
> 2. Oblivious Amplitude Amplification, OR
> 3. Global spacetime formulation (QSVT), OR
> 4. Hybrid classical re-normalization per timestep.
