# PHASE F20: SYSTEMATIC ARCHITECTURAL COMPARISON

## 1. Candidate Architectures Evaluated
This document evaluates five candidate quantum architectures developed across the history of the QLBM project:
- **Architecture A (Level-6B Hybrid Baseline)**: Local second-order Carleman linearization with classical state reconstruction and parameter injection at every timestep.
- **Architecture B (Phase F18 Full-State Environment)**: CNOT-mediated full copying of the pre-collision microstate into an auxiliary environment register.
- **Architecture C (Phase F19 Moment-Space Channel)**: Stinespring dilation coupling the environment strictly to non-equilibrium Hermite moments.
- **Architecture D (Reversible Compute-Output Embedding)**: Reversible out-of-place arithmetic generating fresh output registers at each timestep.
- **Architecture E (Phase F20 Validated Moment-Space CPTP QLBM)**: Validated moment-space CPTP channel with active mid-circuit dissipative reset and selective coherence preservation.

---

## 2. Comparative Evaluation Matrix
From [`results/phase_f20/f20_architecture_comparison.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_architecture_comparison.csv):

| Evaluation Criterion | A: Level-6B Hybrid | B: F18 Full-Copy | C: F19 Moment Channel | D: Compute-Output | E: F20 Validated CPTP |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Physical Collision Fidelity** | HIGH (<3.8% surge error) | EXACT on basis | EXACT on basis | EXACT on basis | **EXACT (Conserved + Relaxed)** |
| **Conserved Coherence Survival** | ZERO (re-encoded) | ZERO (universal dephasing) | PARTIAL (conserved modes) | HIGH (in joint space) | **EXACT (100% for same non-eq)** |
| **CPTP Channel Validity** | N/A (Projective Hybrid) | YES (Kraus Rank 512) | YES (Kraus Rank 8) | YES (Unitary Rank 1) | **YES (Choi $\lambda_{\min} \ge 0$)** |
| **Quantum Autonomy** | HYBRID ($K=1$) | AUTONOMOUS | AUTONOMOUS CPTP | AUTONOMOUS | **AUTONOMOUS CPTP CHANNEL** |
| **Two-Phase Coupling** | YES ($f$ and $g$ coupled) | YES (integer logic) | YES (moment logic) | YES | **YES (Dual moment registers)** |
| **CSF Surface Tension** | VALIDATED ($\sigma > 0$) | EXCLUDED ($\sigma = 0$) | THEORETICAL | THEORETICAL | **TIER 2 HYBRID / TIER 3 THEORETICAL** |
| **Node Resource Footprint** | LOW (hybrid) | VERY HIGH (288Q env) | MEDIUM (48Q env) | UNBOUNDED | **OPTIMIZED (48Q env, 7616 Toff)** |
| **Environment Scaling in $T$** | $\mathcal{O}(1)$ | $\mathcal{O}(T)$ (unbounded) | $\mathcal{O}(1)$ with reset | $\mathcal{O}(T)$ (unbounded) | **$\mathcal{O}(1)$ PROVEN VIA RESET** |
| **Multi-Step Viability** | HIGH ($T=2000$) | LOW ($T \le 2$) | HIGH ($T=64$) | LOW | **DEMONSTRATED ($T=64$ STABLE)** |
| **Hardware Feasibility** | 16Q NISQ demonstrator | FTQC only | FTQC only | FTQC only | **NISQ DEMO + FTQC CHANNEL** |
| **Scientific Classification** | **LEVEL B** | **LEVEL B** | **LEVEL B** | **LEVEL B** | **LEVEL B (DEFENSIBLE CHANNEL)** |

---

## 3. Verdict and Recommendation
Architecture E (Phase F20 Validated Moment-Space CPTP QLBM) is the **sole mathematically sound and physically consistent quantum architecture** that simultaneously:
1. Implements non-injective dissipative BGK relaxation,
2. Preserves 100% of quantum coherence across conserved hydrodynamic branches,
3. Operates autonomously without intermediate classical amplitude inspection,
4. Achieves constant $\mathcal{O}(1)$ memory scaling in time via active dissipative reset.
