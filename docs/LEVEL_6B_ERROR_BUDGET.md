# LEVEL-6B: 9-COMPONENT ERROR BUDGET DECOMPOSITION

**Document**: Error Attribution and Scaling Analysis for Level 6B  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## Complete Error Decomposition Table

| Component | Error Source | Theoretical Scaling | Measured Numerical Magnitude | Impact on Solver |
| :--- | :--- | :---: | :---: | :--- |
| **1. Local Carleman Collision Truncation** | Quadratic low-Mach Taylor expansion of $j_a j_b/\rho$ | $\mathcal{O}(\text{Ma}^2 \frac{\delta\rho}{\rho_0})$ | $1.25 \times 10^{-4}$ | Dominant algorithmic approximation in local collision. |
| **2. Quantum Block-Encoding Dilation** | Sz.-Nagy unitary dilation precision | Machine $\epsilon_{\text{mach}}$ | $2.28 \times 10^{-13}$ | Negligible (exact block embedding). |
| **3. Quantum State Preparation** | Amplitude rotation encoding | $\mathcal{O}(2^{-n_{\text{rot}}})$ | $5.00 \times 10^{-4}$ | Bounded initialization precision. |
| **4. Classical Re-lifting** | Kronecker product $\mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})$ | Machine $\epsilon_{\text{mach}}$ | **$0.00 \times 10^0$** | Exact invariant manifold preservation. |
| **5. Linear Population Streaming** | Spatial shift on 18 linear populations | Exact permutation | **$0.00 \times 10^0$** | Exact spatial transport (zero tensor shift error). |
| **6. Solid Boundary Bounce-Back** | Direction-selective wall reflection | Exact involution $B^2 = I$ | **$0.00 \times 10^0$** | Exact solid boundary reflection. |
| **7. Continuum Surface Force (CSF)** | Brackbill central difference stencil | $\mathcal{O}(\Delta x^2)$ | $1.90 \times 10^{-5}$ | Controlled second-order interface curvature. |
| **8. Gravitational Body Force** | Hydrostatic buoyancy force | Exact linear | **$0.00 \times 10^0$** | Exact vertical gravity acceleration. |
| **9. Grid Discretization** | D2Q9 lattice velocity quadrature | $\mathcal{O}(\Delta x^2)$ | $2.40 \times 10^{-4}$ | Standard hydrodynamic LBM discretization error. |
