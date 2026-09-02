# LEVEL-7: LIMITATIONS & EXPLICIT NON-CLAIMS

**Document**: Scientific Boundaries and Non-Claims for Level 7  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Technical Limitations

1. **Second-Order Low-Mach Truncation**:
   Local Carleman collision truncates convective terms higher than quadratic, introducing an unavoidable low-Mach error scaling as $\mathcal{E} \propto \text{Ma}^2$. The solver is valid for weakly-compressible regimes ($\text{Ma} \le 0.1$).
2. **Success Probability Decay without OAA**:
   Unamplified projective resets cause the raw success probability to decay as $p_{\text{succ}}(K) = \alpha_C^{-2K} \approx (1.06 \times 10^{-2})^K$. Coherent multi-step evolution for $K > 2$ requires Oblivious Amplitude Amplification (OAA) or early Fault-Tolerant Quantum Computing (FTQC).
3. **Hybrid CSF Feedback**:
   Continuum Surface Force (CSF) curvature stencils are evaluated classically and coupled as hybrid feedback every $K$ steps. Fully autonomous on-chip quantum curvature evaluation is not implemented.
4. **Fixed Mean Reference Relaxation**:
   Carleman matrices utilize a fixed mean relaxation $\tau_0$ around $\rho_0 = 1.0$.

---

## 2. Explicit Non-Claims (Prohibited Scientific Statements)

- **DO NOT** claim a "fully quantum, measurement-free, or autonomous dam-break solver".
- **DO NOT** claim "quantum speedup" on classical computers.
- **DO NOT** claim "exact nonlinear Navier-Stokes solution".
- **DO NOT** claim "real physical IBM Quantum execution".
- **DO NOT** claim "O(log N) total computational complexity" from logarithmic qubit count alone.
