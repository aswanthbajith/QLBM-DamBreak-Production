# PHASE F19: COMPUTE-OUTPUT REVERSIBLE EMBEDDING (ARCHITECTURE A)
## Exact Unitary Realization on the Product Register Space

**Document**: Architecture A Compute-Output Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Operator Formulation

$$U_A: |x\rangle |0\rangle_{\text{out}} \mapsto |x\rangle |F(x)\rangle$$

Because the mapping $(x, 0) \mapsto (x, F(x))$ preserves the input state $|x\rangle$, it constitutes an **exact bijective embedding** on $\mathcal{H}_{\text{in}} \otimes \mathcal{H}_{\text{out}}$.

### Properties:
- **Unitarity**: $U_A^\dagger U_A = I_{\text{joint}}$ is exact.
- **Information Loss**: Zero (input state $x$ is preserved in the first register).
- **Multi-Step Memory**: Advancing $T$ timesteps requires $\mathcal{O}(T \cdot N_{\text{pop}})$ qubits unless an environmental dissipative channel is used.
