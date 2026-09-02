# Quantum Lattice Boltzmann Method Architecture

This document describes the mathematical and algorithmic architecture of the direct-encoding Quantum Lattice Boltzmann Method (QLBM) for two-phase dam-break fluid flow.

---

## 1. Algorithmic Flowchart

```
+-------------------------------------------------------------+
|               Classical State Initialization (t=0)          |
|    rho(x,y), alpha(x,y), u(x,y) -> f_eq(x,y), g_eq(x,y)     |
+-------------------------------------------------------------+
                               |
                               v  (Single Quantum State Prep)
+-------------------------------------------------------------+
|              Direct Spatial / Population Encoding           |
|     |psi_0> in H_x (x) H_y (x) H_vel (x) H_phase            |
+-------------------------------------------------------------+
                               |
                               v
               +-------------------------------+
               |   TIME EVOLUTION LOOP (t=1..T)|
               +-------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|            CPTP BGK Quantum Collision Channel (E_BGK)       |
|   Stinespring Dilation: U |x>_S |0>_E = |F(x)>_S |x>_E      |
|   Reduced State: E(rho) = Tr_E [ U (rho (x) |0><0|) U^dag ]  |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               Exact Unitary Spatial Streaming (S)           |
|        Coordinate Wire Permutation: S^dag S = I             |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|             Exact Boundary Bounce-Back Involution (B)       |
|        Solid Mask Velocity Inversion: B^2 = I               |
+-------------------------------------------------------------+
                               |
                               v (Repeat until t = T)
+-------------------------------------------------------------+
|                 Final Measurement Readout (t=T)             |
|   Extract macroscopic moments: rho(x,y), alpha(x,y), u(x,y) |
+-------------------------------------------------------------+
```

---

## 2. Identified Interfaces & Hybrid Control Boundaries

- **State Initialization**: 1 classical preparation at $t=0$.
- **Collision Step**: Open-system CPTP quantum channel $\mathcal{E}_{\text{BGK}}$ representing statistical relaxation of non-equilibrium populations.
- **Streaming Step**: 100% closed unitary spatial permutation ($S^\dagger S = I$).
- **Boundary Step**: 100% closed unitary involution ($B^2 = I$).
- **Intermediate Operations**: 0 intermediate measurements, 0 classical state extractions, 0 population re-encodings during time evolution.
- **Final Readout**: 1 measurement at $t=T$.
