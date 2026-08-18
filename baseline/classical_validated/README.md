# Frozen Ground-Truth Reference: Classical Two-Phase LBM

**Commit Hash**: `0779537`  
**Git Tag**: `classical_validated_v1`  
**Status**: Frozen Ground-Truth Classical Baseline  
**Date**: August 19, 2026  

## 1. Mathematical Formulation
- **Lattice**: D2Q9 velocity-based incompressible LBM for hydrodynamics ($g_i$) and Conservative Allen-Cahn phase field ($h_i$).
- **Properties**: $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$, $\nu(\phi) = \mu(\phi)/\rho(\phi)$.
- **Body Forces**: $\mathbf{F} = \sigma \kappa_I \nabla \phi + (\rho(\phi) - \rho_G)\mathbf{g}_{grav}$.
- **Guo Body Forcing**: Second-order momentum coupling on $g_i$.

## 2. Benchmark Metrics (Martin & Moyce 1952)
- **Mass Conservation**: $< 1.589\%$ maximum relative drift over 2,200 steps.
- **Surge Wavefront**: $L_1 = 1.8426$, $L_2 = 2.1827$, $L_\infty = 3.5833$.
- **Column Height**: $L_1 = 0.3493$, $L_2 = 0.4154$, $L_\infty = 0.5911$.
- **Unit Tests**: 6/6 tests passing in `tests/test_two_phase_physics.py`.
