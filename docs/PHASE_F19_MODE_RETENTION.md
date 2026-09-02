# PHASE F19: MODE-RETAINING EMBEDDING (ARCHITECTURE C)
## Equilibrium and Non-Equilibrium Coordinate Split

**Document**: Architecture C Mode Retention Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Bijective Mode Decomposition

$$U_C: |\mathbf{f}\rangle |0\rangle \mapsto |\mathbf{f}^{\text{eq}}\rangle |\mathbf{f}^{\text{neq}}\rangle$$

where:
$$\mathbf{f}^{\text{neq}} = \mathbf{f} - \mathbf{f}^{\text{eq}}$$

- **Inverse Reconstruction**: $\mathbf{f} = \mathbf{f}^{\text{eq}} + \mathbf{f}^{\text{neq}}$ is exact ($0.00$ error).
- **Constant Memory Footprint**: Requires a fixed $2 \times 288 = 576$ bits per lattice node across all timesteps $T$ ($\mathcal{O}(1)$ memory scaling).
