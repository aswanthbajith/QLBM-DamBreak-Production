# PHASE F20: KRAUS DECOMPOSITION & CHOI MATRIX VERIFICATION

## 1. Kraus Representation
The moment-space channel $\mathcal{E}_C$ can be written in operator-sum (Kraus) form:
$$\mathcal{E}_C(\rho) = \sum_k K_k \rho K_k^\dagger$$
where each Kraus operator $K_k$ corresponds to projecting the environment onto a distinct basis state $|k\rangle_E$:
$$K_k = \langle k |_E V_m |0\rangle_E = \sum_{\mathbf{m}: e(\Delta \mathbf{m}_{\text{neq}}) = k} |\mathbf{m}^*\rangle \langle \mathbf{m}|$$

### Properties Verified in [`results/phase_f20/f20_kraus.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_kraus.csv):
1. **Kraus Rank**: For a finite-dimensional model with $d_{\text{neq}}$ distinct non-equilibrium deviations, the Kraus rank is exactly equal to the number of distinct environment states:
   $$R_K = d_{\text{neq}} \le 8$$
   This represents a drastic compression from the full-copying F18 baseline ($R_K = 512$).
2. **Completeness Relation**:
   $$\sum_k K_k^\dagger K_k = I_S$$
   The trace-preservation error is $\| \sum K_k^\dagger K_k - I_S \| < 10^{-15}$ (exact to machine precision).

---

## 2. Choi-Jamiołkowski Isomorphism and Complete Positivity
The Choi matrix $J_{\mathcal{E}}$ associated with channel $\mathcal{E}_C$ is defined by acting on one half of a maximally entangled state $|\Phi^+\rangle = \frac{1}{\sqrt{d_S}} \sum_{i=0}^{d_S-1} |i\rangle |i\rangle$:
$$J_{\mathcal{E}} = (I \otimes \mathcal{E}_C)(|\Phi^+\rangle\langle\Phi^+|) = \frac{1}{d_S} \sum_{i, j=0}^{d_S-1} |i\rangle\langle j| \otimes \mathcal{E}_C(|i\rangle\langle j|)$$

### Verification Criteria:
1. **Hermiticity**:
   $$\|J_{\mathcal{E}} - J_{\mathcal{E}}^\dagger\| = 0.00 \times 10^0 \implies \mathbf{EXACT\ HERMITICITY}$$
2. **Complete Positivity**:
   By Choi's theorem, $\mathcal{E}$ is completely positive if and only if $J_{\mathcal{E}} \succeq 0$.
   Numerical diagonalization recorded in [`results/phase_f20/f20_choi.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_choi.csv) confirms:
   $$\lambda_{\text{min}}(J_{\mathcal{E}}) = 0.000000 \ge -10^{-15} \implies \mathbf{EXACT\ COMPLETE\ POSITIVITY}$$
   All 64 eigenvalues are non-negative real numbers.
3. **Trace Preservation**:
   $$\text{Tr}_{\text{out}}(J_{\mathcal{E}}) = \frac{1}{d_S} I_{\text{in}} \implies \|\text{Tr}_{\text{out}}(J_{\mathcal{E}}) - \frac{1}{d_S} I\| < 10^{-15} \implies \mathbf{EXACT\ TRACE\ PRESERVATION}$$

---

## 3. Summary CPTP Table
From [`results/phase_f20/f20_cptp.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_cptp.csv):

| Mathematical Criterion | Error Norm | Verification Status |
| :--- | :---: | :---: |
| Trace Preservation $\sum K_k^\dagger K_k = I$ | $0.00 \times 10^0$ | **PASS (Exact)** |
| Complete Positivity $\lambda_{\text{min}}(J) \ge 0$ | $0.00 \times 10^0$ | **PASS (Exact)** |
| Hermiticity Preservation $\mathcal{E}(\rho)^\dagger = \mathcal{E}(\rho)$ | $0.00 \times 10^0$ | **PASS (Exact)** |
| Density Matrix Trace Preservation $\text{Tr}(\mathcal{E}(\rho)) = 1$ | $0.00 \times 10^0$ | **PASS (Exact)** |
| Kraus Completeness Relation | $0.00 \times 10^0$ | **PASS (Exact)** |
