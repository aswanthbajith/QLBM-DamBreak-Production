# PHASE 5 PHYSICAL OBSERVABLE DEFINITIONS & MEASUREMENT PROTOCOLS

**Status**: Official Specification  
**Date**: 2026-08-19  

---

## 1. Physical Observable Mathematical Definitions

### 1.1 Surge Front Position ($x^*$)
* **Mathematical Definition**: The non-dimensionalized maximum downstream horizontal coordinate of the advancing liquid front at the bottom boundary:
  $$x^*(t) = \frac{x_{\text{front}}(t)}{H_{\text{dam}}}$$
* **Lattice Subspace Implementation**:
  $$x_{\text{front}} = \max \{ x \in [0, N_x-1] \mid \phi(x, y_{\text{floor}}) > 0.5 \}$$
  where $\phi(x, y) = \sum_{q=0}^8 h_q(x, y)$.
* **Measurement Basis**: Computational basis measurements on the phase-field registers $|h_q(x, y)\rangle$.
* **Finite-Shot Estimator**:
  $$\hat{\phi}(x, y) = \sum_{q=0}^8 \hat{h}_q(x, y) + \mathcal{N}\left(0, \frac{1}{N_s}\right)$$
  $$\hat{x}^* = \frac{\max \{ x \mid \hat{\phi}(x, y_{\text{floor}}) > 0.5 \}}{H_{\text{dam}}}$$

### 1.2 Residual Column Height ($h^*$)
* **Mathematical Definition**: The non-dimensionalized vertical height of the remaining liquid column against the back wall ($x=0$):
  $$h^*(t) = \frac{y_{\text{col}}(t)}{H_{\text{dam}}}$$
* **Lattice Subspace Implementation**:
  $$y_{\text{col}} = \max \{ y \in [0, N_y-1] \mid \phi(x_{\text{wall}}, y) > 0.5 \}$$

### 1.3 Total Fluid Mass ($M$)
* **Mathematical Definition**: Total integrated liquid phase volume in the computational domain:
  $$M(t) = \int_\Omega \phi(\mathbf{x}, t) \, d\mathbf{x} = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \phi(x, y)$$
* **Amplitude Estimation Potential**:
  $M$ corresponds directly to the state amplitude $\|P_{\phi} |\Psi\rangle\|^2$. Using Quantum Amplitude Estimation (QAE), $M$ can theoretically be estimated to precision $\epsilon$ with $\mathcal{O}(1/\epsilon)$ queries, compared to $\mathcal{O}(1/\epsilon^2)$ classical Monte Carlo sampling.
* **Demonstrated Implementation in Phase 5**: Finite-shot Monte Carlo simulation with validated $1/\sqrt{N_s}$ SQL scaling.

### 1.4 Downstream Impact Wall Pressure ($p$)
* **Mathematical Definition**: Pressure measured at downstream sensor node $(x_{\text{sensor}}, y_{\text{sensor}})$:
  $$p(\mathbf{x}, t) = c_s^2 \rho(\mathbf{x}, t) = c_s^2 \sum_{q=0}^8 g_q(\mathbf{x}, t)$$
  where $c_s^2 = 1/3$.
