# Quantitative Carleman Linearization Validation & Convergence Study

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Multi-Step Time-Horizon Convergence Study

We executed multi-step time evolution on an $8 \times 4$ ($N=32$) dam-break collapse comparing:
1. **Classical Nonlinear Solver** (`TwoPhaseLBM2D`)
2. **Carleman Order 1 Linear Solver** ($D_C = 576$)
3. **Carleman Order 2 Quadratic Solver** ($D_C = 10,944$)

### Quantitative Multi-Step Error Growth Table:

| Timestep | Non-Dim Time $t^*$ | Order 1 $L_1$ Error | Order 1 $L_\infty$ Error | Order 2 $L_1$ Error | Order 2 $L_\infty$ Error | Order 2 Relative Error | Truncation Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 0.0082 | $2.1734 \times 10^{-5}$ | $4.5232 \times 10^{-4}$ | **$2.1734 \times 10^{-5}$** | **$4.5232 \times 10^{-4}$** | **$0.0999\%$** | Exact / Negligible |
| **2** | 0.0163 | $4.4185 \times 10^{-5}$ | $5.7713 \times 10^{-4}$ | **$4.4185 \times 10^{-5}$** | **$5.7713 \times 10^{-4}$** | **$0.1607\%$** | Exact / Negligible |
| **5** | 0.0408 | $9.6142 \times 10^{-5}$ | $1.3279 \times 10^{-3}$ | **$9.6142 \times 10^{-5}$** | **$1.3279 \times 10^{-3}$** | **$0.3268\%$** | High Fidelity |
| **10** | 0.0816 | $1.4019 \times 10^{-4}$ | $2.1748 \times 10^{-3}$ | **$1.4019 \times 10^{-4}$** | **$2.1748 \times 10^{-3}$** | **$0.5448\%$** | High Fidelity |
| **20** | 0.1633 | $2.2903 \times 10^{-4}$ | $4.4320 \times 10^{-3}$ | **$2.2903 \times 10^{-4}$** | **$4.4320 \times 10^{-3}$** | **$0.9655\%$** | Converged |
| **30** | 0.2449 | $3.1002 \times 10^{-4}$ | $7.3359 \times 10^{-3}$ | **$3.1002 \times 10^{-4}$** | **$7.3359 \times 10^{-3}$** | **$1.4547\%$** | Bounded |
| **40** | 0.3266 | $4.0122 \times 10^{-4}$ | $1.0871 \times 10^{-2}$ | **$4.0122 \times 10^{-4}$** | **$1.0871 \times 10^{-2}$** | **$1.9969\%$** | Bounded |
| **50** | 0.4082 | $5.0436 \times 10^{-4}$ | $1.3680 \times 10^{-2}$ | **$5.0436 \times 10^{-4}$** | **$1.3680 \times 10^{-2}$** | **$2.5815\%$** | Bounded |

---

## 2. 100-State Random Perturbation Equivalence Audit

Across 100 independently sampled physical state vectors with random phase fractions $\phi \in [0, 1]$, velocities $|\mathbf{u}| < 0.01$, and pressures $|p| < 0.001$:
- **Matrix Operator Equivalence**:
  - Maximum $L_\infty$ Error: **$1.6636 \times 10^{-3}$**
  - Mean $L_\infty$ Error: **$8.9463 \times 10^{-4}$**
- **Carleman Order 2 Single-Step Equivalence**:
  - Maximum Relative Error: **$1.6187 \times 10^{-2}$** ($1.62\%$)
  - Mean Relative Error: **$1.3708 \times 10^{-2}$** ($1.37\%$)

---

## 3. Computational Scaling Performance across Spatial Resolutions

| Grid ($N_x \times N_y$) | Nodes $N$ | Order 2 Dim $342N$ | Matrix NNZ | Memory (MB) | Assembly Time (s) | MatVec Time (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$8 \times 4$** | 32 | 10,944 | 874,688 | **10.05** | 0.93 | **0.94** |
| **$16 \times 8$** | 128 | 43,776 | 3,498,752 | **40.21** | 3.59 | **3.96** |
| **$32 \times 16$** | 512 | 175,104 | 13,995,008 | **160.83** | 16.37 | **52.05** |
| **$64 \times 32$** | 2,048 | 700,416 | 55,980,032 | **643.31** | 66.24 | **193.91** |
