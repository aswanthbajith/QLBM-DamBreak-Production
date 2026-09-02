# PHASE F20: KRAUS OPERATOR DERIVATION & TRACE PRESERVATION
## Rigorous Proof of CPTP Completeness

**Document**: Kraus Derivation & Trace Preservation Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Derivation of Kraus Operators

From the Stinespring dilation unitary $U |x\rangle_S |0\rangle_E = |F(x)\rangle_S |x\rangle_E$, the Kraus operators are:
$$K_\mu = \langle \mu|_E U |0\rangle_E = |F(\mu)\rangle \langle \mu| \quad \forall \mu \in \mathcal{X}$$

### Trace Preservation Proof:
$$\sum_{\mu \in \mathcal{X}} K_\mu^\dagger K_\mu = \sum_{\mu \in \mathcal{X}} (|\mu\rangle \langle F(\mu)|) (|F(\mu)\rangle \langle \mu|) = \sum_{\mu \in \mathcal{X}} |\mu\rangle \langle \mu| = I_S$$

$$\left\| \sum_{\mu} K_\mu^\dagger K_\mu - I_S \right\|_2 = 0.0000 \times 10^0$$

The channel is **strictly trace-preserving**.
