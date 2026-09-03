# FINAL ARCHITECTURE MAP
## Structural Layout of the Complete Quantum Two-Phase LBM Ecosystem

```text
                                  +---------------------------------------+
                                  |    Two-Phase Dam-Break Hydrodynamics   |
                                  +---------------------------------------+
                                                      |
                                    +-----------------+-----------------+
                                    |                                   |
                                    v                                   v
                      +---------------------------+       +---------------------------+
                      | Classical Reference (L4)  |       | Level-6B Hybrid Baseline  |
                      | level4_two_phase.py       |       | level6b_hybrid_solver.py  |
                      | Martin & Moyce Benchmark  |       | SHA-256: 2a306f5a413945...|
                      +---------------------------+       +---------------------------+
                                                                        |
                                    +-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-------------------------------+               +-------------------------------+
|  Scalable Reversible Circuit  |               |    NISQ Hardware Demonstrator |
|  (Phases F27–F31)             |               |    (Phases F33–F38)           |
|  f29_scalable_circuit.py      |               |    f33_hardware_demo.py       |
|  f31_reduced_architecture.py  |               |    f38_qpu_executor.py        |
|  560 qubits/node, Q4.16       |               |    16 qubits (2x2), depth 19  |
|  C^-1 C = I exact unitary     |               |    Runs on IBM FakeSherbrooke |
+-------------------------------+               +-------------------------------+
            |                                               |
            v                                               v
+-------------------------------+               +-------------------------------+
| Fault-Tolerant Scaling Study  |               | Real IBM Quantum Execution    |
| (128x64 Mesh, 4.19M Qubits)   |               | (Double Opt-In Guarded Gate)  |
+-------------------------------+               +-------------------------------+
```
