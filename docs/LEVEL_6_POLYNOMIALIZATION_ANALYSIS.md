# LEVEL-6: POLYNOMIALIZATION & RATIONAL FUNCTION ANALYSIS

This document provides a systematic analysis of the 8 non-polynomial terms present in the Level-4 classical reference solver and evaluates candidate approximation strategies for Carleman linearization and quantum circuit synthesis.

---

## 1. Analysis of the 8 Non-Polynomial Components

### A. Reciprocal Density ($1/\rho$)
- **Physical Context**: Appears in convective momentum $\mathbf{u} = \mathbf{j}/\rho$ and hydrodynamic equilibrium $f_i^{\text{eq}} \propto j_a j_b / \rho$.
- **Taylor Expansion**: For weakly-compressible flow with density fluctuation $\delta\rho = \rho - \rho_0 \ll \rho_0$:
  $$\frac{1}{\rho} = \frac{1}{\rho_0} \left( 1 - \frac{\delta\rho}{\rho_0} + \left(\frac{\delta\rho}{\rho_0}\right)^2 - \dots \right)$$
- **Approximation Error**: Truncation at 0th order introduces relative error $\mathcal{O}(\delta\rho/\rho_0) \sim \mathcal{O}(\text{Ma}^2)$. For dam-break flow with $\text{Ma} \le 0.08$, truncation error is $< 0.64\%$.
- **Auxiliary Variable Lifting Alternative**: Introduce auxiliary scalar $v = 1/\rho$, adding constraint equation $\frac{\partial v}{\partial t} = -v^2 \frac{\partial \rho}{\partial t}$. This increases Carleman state dimension by $N$ and introduces quadratic auxiliary terms.

### B. Reciprocal Viscosity Relaxation ($1/\tau(\alpha)$)
- **Physical Context**: Appears in collision parameter $\omega_f(\alpha) = 1/(3\nu(\alpha) + 0.5) = 1/(3(\alpha\nu_L + (1-\alpha)\nu_G) + 0.5)$.
- **Fixed Reference Approximation**: Set $\tau_0 = 3\bar{\nu} + 0.5$ where $\bar{\nu} = 0.5(\nu_L + \nu_G)$. For equal kinematic viscosities ($\nu_L = \nu_G = 0.05$), $\tau_f = 0.65$ is **IDENTICALLY CONSTANT** and the error is **ZERO** ($E = 0$).
- **Taylor Expansion for Viscosity Contrast**: $\omega_f(\alpha) = \omega_0 [1 - 3\Delta\nu(\alpha - \alpha_0)/\tau_0 + \dots]$.

### C. Convective Momentum Flux ($j_a j_b / \rho$)
- **Level-5 Second-Order Representation**: $E_2^{(f)} = \frac{w_i}{\rho_0} [4.5 (\mathbf{c}_i \cdot \mathbf{j})^2 - 1.5 |\mathbf{j}|^2]$.
- **Mathematical Nature**: Exact quadratic polynomial in the momentum tensor $\mathbf{j} \otimes \mathbf{j} = \sum_{j,k} (\mathbf{c}_j \otimes \mathbf{c}_k) f_j f_k$.
- **Error**: Bounded by $\mathcal{O}(\text{Ma}^2 \delta\rho / \rho_0)$.

### D. Interfacial Normal ($\mathbf{n} = \nabla\alpha / |\nabla\alpha|$) & Curvature ($\kappa = -\nabla\cdot\mathbf{n}$)
- **Mathematical Nature**: Involves spatial gradients $\nabla\alpha$, Euclidean norm $\sqrt{(\partial_x\alpha)^2 + (\partial_y\alpha)^2}$, and non-local divergence.
- **Approximation / Quantum Treatment**:
  - *Strategy 1 (Reversible Arithmetic / Oracle)*: Requires multi-qubit division and square root circuits (depth $> 10^5$, $> 50$ ancillas per node).
  - *Strategy 2 (Polynomial Gradient-Square Stencil)*: Approximate $|\nabla\alpha| \approx 1$ in the interface core $\alpha \approx 0.5$, reducing to $\kappa \approx -\nabla^2 \alpha$.
  - *Strategy 3 (Hybrid Classical Preprocessing)*: Evaluate $\mathbf{F}_s = \sigma\kappa\nabla\alpha$ classically after observable readout or via hybrid oracle feedback.

### E. Phase Fraction Clipping ($\text{clip}(\alpha, 0, 1)$) & Velocity Clamping ($|\mathbf{u}| \le 0.15$)
- **Mathematical Nature**: Piecewise linear / hard saturation functions.
- **Quantum Treatment**: Cannot be represented by linear unitary or Carleman operators. Natural regularization occurs via postselection or periodic quantum observable calibration.

---

## 2. Comparison of Polynomialization Strategies

| Strategy | Mathematical Accuracy | State Dimension Overhead | Ancilla / Qubit Overhead | Implementation Feasibility | Recommended Role |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Truncated Low-Mach Taylor Expansion** | High for $\text{Ma} \le 0.1$ ($< 1\%$ error) | **None** ($d_C = 342N$) | **Minimal** (1 ancilla for dilation) | **High** (Tested & Verified) | **Core Carleman Collision** |
| **2. Auxiliary Variable Lifting ($v = 1/\rho$)** | Exact for smooth $\rho$ | Moderate ($d_C \approx 500N$) | Moderate (+2 logical qubits) | Moderate | Future Refinement |
| **3. Reversible Non-Polynomial Quantum Oracle** | Exact | High | Extreme ($> 50$ work qubits/site) | Low (Impractical for NISQ/Early FTQC) | Long-Term Theoretical |
| **4. Hybrid Classical CSF Evaluation** | Exact to classical mesh stencil | **None** | **None** | **High** | **Surface Tension Forcing** |
