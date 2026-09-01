# LEVEL-6B: SYSTEM ARCHITECTURE SPECIFICATION
## Hybrid K=1 Local-Carleman Two-Phase QLBM Architecture

```text
               ┌────────────────────────────────────────────────────────┐
               │    1. Classical Initialization & State Memory z_t      │
               │       z(x, t) = [f_0..f_8, g_0..g_8]^T in R^18         │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    2. Local Quadratic Kronecker Lifting                │
               │       Y(x, t) = [z(x, t); z(x, t) (x) z(x, t)] in R^342│
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    3. Quantum Carleman Collision Block (K = 1)         │
               │       z*(x, t) = P (alpha_C U_C) P^T Y(x, t)           │
               │       Executed via 10-qubit Sz.-Nagy Unitary Dilation  │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    4. Classical State Reconstruction of Populations    │
               │       Extract f*(x, t) and g*(x, t)                    │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    5. Linear Spatial Streaming & Bounce-Back Boundary  │
               │       f_i(x + c_i) = f*_i(x), g_i(x + c_i) = g*_i(x)   │
               │       Solid wall involution B on perimeter boundaries  │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    6. Continuum Surface Force & Body Force Feedback    │
               │       F_s = sigma * kappa * grad(alpha)                │
               │       F_g = (rho - rho_G) * g_acc                      │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │    7. Advance to Timestep t+1                          │
               └────────────────────────────────────────────────────────┘
```
