# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Quantum State Representation & Amplitude Convention Audit

**Document**: Physical Interpretation of Quantum State Amplitudes & Subspace Invariance  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Amplitude Convention

In the Direct Spatial/Population Quantum State:
$$|\Psi\rangle = \frac{1}{\mathcal{N}} \left( \sum_{x,y,i} f_i(x,y) |x,y,i,0\rangle + \sum_{x,y,i} g_i(x,y) |x,y,i,1\rangle \right)$$
where $\mathcal{N} = \sqrt{\sum_{x,y,i} (|f_i|^2 + |g_i|^2)}$.

### Crucial Distinction: Linear Amplitude vs Probability Encoding
- **Amplitude Convention**: Amplitudes $\langle x,y,i,p|\Psi\rangle$ are directly proportional to the physical kinetic populations ($f_i$ or $g_i$), NOT their square roots ($\sqrt{f_i}$).
- **Why Linear Amplitude Encoding is Mandatory for Kinetic LBM**:
  1. In the Boltzmann equation, macroscopic mass density and momentum are **linear sums** of populations: $\rho = \sum_i f_i$, $\mathbf{j} = \sum_i f_i \mathbf{c}_i$.
  2. Spatial streaming $S$ is a **linear permutation** of populations: $f_i^*(\mathbf{x} + \mathbf{c}_i) = f_i(\mathbf{x})$.
  3. If amplitudes encoded $\sqrt{f_i}$, linear streaming on $\sqrt{f_i}$ would be preserved, but macroscopic density $\rho = \sum (\sqrt{f_i})^2$ would require computing Born rule measurement probabilities ($p_i = |\langle i|\Psi\rangle|^2$). However, the linear summation for momentum $\mathbf{j} = \sum c_i (\sqrt{f_i})^2$ could not be evaluated via simple quantum linear interference!
  4. Linear amplitude encoding allows unitary permutation streaming $S$ and boundary involution $B$ to act with zero distortion on the exact physical distributions.

---

## 2. Invalid / Idle Velocity Subspace Handling

The discrete velocity register uses $n_{\text{vel}} = 4$ qubits ($2^4 = 16$ states), whereas D2Q9 uses only 9 velocities ($|0\rangle \dots |8\rangle$).
- **States $|9\rangle \dots |15\rangle$**: Represent an unphysical padding subspace.
- **Handling in Quantum Operators**:
  1. **State Preparation**: Initialized to strictly $0.0$ amplitude.
  2. **Streaming Operator ($S$)**: Explicitly acts as the **identity operator** on $|9\rangle \dots |15\rangle$: $S |x, y, i \ge 9, p\rangle = |x, y, i, p\rangle$.
  3. **Boundary Operator ($B$)**: Explicitly acts as the **identity operator** on $|9\rangle \dots |15\rangle$: $B |x, y, i \ge 9, p\rangle = |x, y, i, p\rangle$.
- **Numerical Verification**: Amplitude leakage into $|9\rangle \dots |15\rangle$ was tested across multi-step evolution in `test_audit_test_c_subspace_containment()` and verified to be strictly **$< 10^{-15}$** (machine epsilon).
