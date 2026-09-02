# LEVEL-7: OBLIVIOUS AMPLITUDE AMPLIFICATION (OAA) AUDIT
## First-Principles Trigonometric Derivation, Exact Query Counts, and Resource Overhead

**Document**: Rigorous Mathematical Audit of Amplitude Amplification Claims  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. First-Principles Trigonometric Derivation

Let $U_C$ be a unitary block encoding of $C_2$ with normalization factor $\alpha_C = 9.7321$ (as constructed with power-of-two padding in Level-6A/7).
The unamplified one-step postselection success probability is:

$$p_0 = \frac{1}{\alpha_C^2} = \frac{1}{9.7321^2} \approx 0.010558 \quad (1.056\%)$$

The initial Grover rotation angle in the 2D invariant subspace is:

$$\theta = \arcsin\left(\sqrt{p_0}\right) = \arcsin\left(\frac{1}{\alpha_C}\right) = 0.102935 \text{ rad} \quad (5.898^\circ)$$

After $m$ Grover / OAA iterations, the exact success probability is:

$$p_m = \sin^2\big((2m + 1)\theta\big)$$

---

## 2. Exact Step-by-Step Iteration Table

| Iteration ($m$) | Subspace Multiplier ($2m+1$) | Angle $(2m+1)\theta$ (rad) | Success Probability $p_m$ | Forward $U_C$ Calls | Inverse $U_C^\dagger$ Calls | Reflection Ops ($R$) | Total Unitaries | Total Circuit Ops |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$0$** | 1 | $0.1029$ | $1.06\%$ | 1 | 0 | 0 | 1 | **1** |
| **$1$** | 3 | $0.3088$ | $9.24\%$ | 2 | 1 | 2 | 3 | **5** |
| **$2$** | 5 | $0.5147$ | $24.23\%$ | 3 | 2 | 4 | 5 | **9** |
| **$3$** | 7 | $0.7205$ | $43.53\%$ | 4 | 3 | 6 | 7 | **13** |
| **$4$** | 9 | $0.9264$ | $63.92\%$ | 5 | 4 | 8 | 9 | **17** |
| **$5$** | 11 | $1.1323$ | $81.97\%$ | 6 | 5 | 10 | 11 | **21** |
| **$6$** | 13 | $1.3382$ | $94.68\%$ | 7 | 6 | 12 | 13 | **25** |
| **$7$** | **15** | **$1.5440$** | **$99.93\%$** | **8** | **7** | **14** | **15** | **29** |
| **$8$** | 17 | $1.7499$ | $96.83\%$ | 9 | 8 | 16 | 17 | **33** |

---

## 3. Scientific Audit Findings on OAA Claims

1. **Deconstruction of the "8 Queries" Claim**:
   The previous report claimed *"8 queries achieves >99%"*.
   - **Audited Truth**: $m = 7$ iterations requires **8 forward $U_C$ queries**, but MUST also execute **7 inverse $U_C^\dagger$ queries** and **14 reflection operators**, bringing the true total to **29 circuit operations** (15 unitary block encodings).
   - Stating "8 queries" without counting $U_C^\dagger$ and reflections is a $3.6\times$ underestimate of circuit operations.
2. **OAA Circuit Depth Explosion**:
   - Single unamplified block depth on IBM FakeSherbrooke: $3,763,998$.
   - Full OAA-amplified step depth ($m=7$): $15 \times 3,763,998 + 14 \times 50 \approx \mathbf{56,460,670 \text{ Gates/Depth}}$.
   - Two-qubit ECR gates per amplified step: $15 \times 831,053 + 14 \times 20 \approx \mathbf{12,466,075 \text{ ECR Gates}}$.
3. **Conclusion**:
   OAA successfully boosts success probability from $1.06\%$ to $99.93\%$, but introduces a **$15\times$ multiplier** in circuit depth, cementing Architecture 7A strictly as a **Fault-Tolerant Quantum Computing (FTQC)** algorithm.
