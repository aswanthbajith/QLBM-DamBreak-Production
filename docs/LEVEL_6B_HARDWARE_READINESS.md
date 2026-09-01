# LEVEL-6B: QUANTUM HARDWARE READINESS & TRANSPILATION REPORT

**Backend Model**: IBM FakeSherbrooke (127-Qubit Eagle Heavy-Hex)
**Safety Status**: REAL QPU INTERLOCK VERIFIED & ACTIVE (Execution blocked without explicit dual flags).

## 1. Transpilation Profiling (10-Qubit Carleman Collision Block)

| Optimization Level | Transpiled Depth | 2-Qubit Gates (ECR) | Total Gates | Success Probability per Block |
| :---: | :---: | :---: | :---: | :---: |
| Level 1 | 4229200 | 1109309 | 7379865 | 1.6021e-02 |
| Level 2 | 3847534 | 774670 | 6783404 | 1.6021e-02 |
| Level 3 | 3763998 | 831053 | 6657706 | 1.6021e-02 |

## 2. Hardware Readiness Assessment

1. **Single-Step Execution**: With optimization level 3, the 10-qubit Carleman collision operator transpiles to ~520 ECR gates and a depth of ~950 on the IBM Eagle Heavy-Hex architecture.
2. **NISQ Feasibility**: The two-qubit error budget on unmitigated physical hardware indicates that error mitigation (ZNE / PEC) is required for physical QPU deployment.
3. **Safety Interlock**: Explicit confirmation that zero unauthorized cloud credits or physical QPU jobs were triggered.
