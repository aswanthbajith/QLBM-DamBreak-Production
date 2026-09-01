# PHASE 15 EXPERIMENTAL METHODS & SCIENTIFIC PROTOCOL

**Status**: Verified Reproducible Protocol  
**Date**: 2026-08-19  

---

## 1. Experimental Methodology
1. **Classical Fluid Ground Truth**: D2Q9 LBM with conservative Allen-Cahn phase-field interface tracking.
2. **Carleman Linearization**: Local quadratic lifting ($D_C = 342 N$) yielding exact sparse matrix representation.
3. **Structured Quantum Oracles**: Reversible spatial streaming permutation $\mathcal{O}(\log N)$ + local collision rotation $\mathcal{O}(1)$.
4. **Hardware Transpilation**: IBM Eagle-127 Heavy-Hex basis gate mapping (`cx, rz, sx, x`).
5. **Measurement & Readout**: Projective computational basis sampling $+ M_3$ matrix inversion $+ ZNE$ zero-noise extrapolation.
