# LEVEL-6: COMPLETE 12-COMPONENT ERROR BUDGET & PROPAGATION ANALYSIS

**Data Reference**: [`results/level6_error_budget.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/level6_error_budget.csv)  
**Objective**: Comprehensive analytical and numerical error decomposition across physical modeling, mathematical linearization, and quantum circuit execution.

---

## 1. The 12 Identified Sources of Error

| Error Component | Source & Mathematical Nature | Scaling with Simulation Parameters | Typical Magnitude ($N_t=10, 64\times 32$) |
| :--- | :--- | :---: | :---: |
| **1. Classical Discretization Error** | Spatial/temporal finite difference grid truncation | $\mathcal{O}(\Delta x^2 \sqrt{N_t})$ | $1.2 \times 10^{-4}$ |
| **2. LBM BGK Model Error** | Discrete D2Q9 velocity quadrature approximation | $\mathcal{O}(\text{Ma}^2)$ | $2.5 \times 10^{-4}$ |
| **3. Low-Mach Taylor Expansion** | Approximation of $1/\rho \approx 1/\rho_0$ in momentum flux | $\mathcal{O}(N_t \cdot \text{Ma}^2 \frac{\delta\rho}{\rho_0})$ | $1.25 \times 10^{-4}$ |
| **4. Carleman Truncation Error** | Unclosed degree-3 & degree-4 terms in $C_2$ | $\mathcal{O}(N_t \cdot \text{Ma}^3)$ | $2.5 \times 10^{-4}$ |
| **5. Polynomial Equilibrium Error** | Quadratic truncation of Maxwell-Boltzmann distribution | $\mathcal{O}(\text{Ma}^3)$ | $6.2 \times 10^{-6}$ |
| **6. Surface Tension Stencil Error** | Discrete central difference curvature $\kappa$ | $\mathcal{O}(\Delta x^2)$ | $1.9 \times 10^{-5}$ |
| **7. Solid Boundary Bounce-Back Slip** | Half-way boundary placement velocity slip | $\mathcal{O}(\Delta x)$ | $3.1 \times 10^{-4}$ |
| **8. Block-Encoding Dilation Error** | Sz.-Nagy spectral matrix square root truncation | Machine precision $\epsilon_{\text{mach}}$ | $1.28 \times 10^{-14}$ |
| **9. QSVT Inversion Error** | Polynomial Chebyshev approximation to $1/x$ | Target user precision $\epsilon$ | $1.0 \times 10^{-3}$ |
| **10. Quantum State Preparation** | Amplitude initialization rotation precision | $\mathcal{O}(2^{-n_{\text{rot}}})$ | $5.0 \times 10^{-4}$ |
| **11. Statistical Shot Noise** | Finite shot sampling in quantum observable readout | $\mathcal{O}(1/\sqrt{N_{\text{shots}}})$ | $1.0 \times 10^{-2}$ (for $10^4$ shots) |
| **12. Hardware Decoherence & Gate Noise** | 2-qubit CNOT / ECR depolarizing gate error | $1 - (1 - \epsilon_{2Q})^{N_{\text{gates}}}$ | $10\% - 95\%$ (unmitigated NISQ) |

---

## 2. Key Findings & Dominant Error Bottlenecks

1. **Algorithmic vs. Statistical Error**:
   - Total algorithmic modeling error (discretization + Carleman + low-Mach + QSVT) remains strictly bounded below **$1.05\%$** up to $N_t = 100$.
   - The dominant source of classical-quantum divergence on quantum simulators/devices is **statistical shot noise** ($\approx 1.0\%$ for $10^4$ shots) and **unmitigated physical hardware noise**.
2. **Carleman Stability**: The second-order Carleman truncation error $\mathcal{O}(N_t \cdot \text{Ma}^3)$ remains negligible ($< 0.25\%$) because the low-Mach dam-break flow operates at $\text{Ma} \le 0.05$.
