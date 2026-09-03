# FINAL END-TO-END DEPENDENCY GRAPH
## Complete Import, Data-Flow, and Computational Boundary Trace

**Branch**: `consolidation/final-working-prototype`  
**Target Solvers**:
1. **Primary Executable Demonstrator (NISQ)**: `quantum/f38_qpu_executor.py` & `quantum/f33_hardware_demo.py`
2. **Primary Scalable Architecture (FTQC)**: `quantum/f31_reduced_architecture.py` & `quantum/f29_scalable_circuit.py`
3. **Primary Physical Reference (Classical / Hybrid)**: `classical/level4_two_phase.py` & `quantum/level6b_hybrid_solver.py`

---

## 1. Primary Executable Quantum Demonstrator Path (F33–F38)

```text
[scripts/run_phase_f38_qpu.py] or [scripts/run_phase_f38_validation.py]
    │
    ▼
[quantum/f38_qpu_executor.py]
    │
    ├── Imports:
    │   ├── qiskit (QuantumCircuit, QuantumRegister, ClassicalRegister, transpile)
    │   ├── quantum.f33_hardware_demo :: F33HardwareDamBreakDemo
    │   ├── quantum.f38_backend_discovery :: F38BackendDiscovery
    │   └── quantum.f38_observables_reconstruction :: F38ObservablesReconstructor
    │
    ▼
[quantum/f33_hardware_demo.py] :: build_timestep_circuit()
    │
    ├── 1. State Preparation [QUANTUM]:
    │   └── quantum.f33_state_preparation :: F33StatePreparation.build_dam_break_initial_state()
    │       └── Pauli-X computational-basis initialization (100% preparation fidelity)
    │
    ├── 2. Reversible Collision & CSF [QUANTUM]:
    │   └── Local 2Q entangling CX + Rz(pi/4) + CX gates and cross-node CZ phase coupling
    │
    ├── 3. Coordinate Streaming Permutation [QUANTUM]:
    │   └── Unitary SWAP gate networks permuting node population registers
    │
    ├── 4. Bounce-Back Wall Boundaries [QUANTUM]:
    │   └── Pauli-X and Pauli-Z involutions on solid boundary registers
    │
    └── 5. Terminal Readout [QUANTUM -> CLASSICAL]:
        └── Standard computational-basis projective measurement: circ.measure(q_sys, c_meas)
```

### Computational Classification of the Demonstrator Pipeline:
- **Classical Initialization Only**: Lattice grid dimensions ($N_x \times N_y$), shot count ($4,096$), and initial fluid column geometry ($x < N_x/2$).
- **Pure Quantum Circuit Evolution**: Zero intermediate measurements; zero classical feedback; zero mid-circuit classical evaluation. All operations between state preparation and final measurement are unitary quantum gates.
- **Terminal Readout Only**: Computational-basis bitstrings are sampled and decoded by `quantum/f38_observables_reconstruction.py` into macroscopic fields $\hat{\rho}(x,y)$, $\hat{\alpha}(x,y)$, and standard errors $\sigma_\rho$.

---

## 2. Scalable Fault-Tolerant Reversible Architecture Path (F27–F31)

```text
[quantum/f31_reduced_architecture.py] :: F31ResourceReducedQuantumCircuit
    │
    ├── Imports:
    │   ├── classical.d2q9 (C_X, C_Y, OPPOSITE)
    │   └── quantum.f27_local_node_circuit :: F27LocalNodeCircuit
    │
    ▼
[quantum/f27_local_node_circuit.py] :: execute_forward_stinespring_node()
    │
    ├── 1. Reversible Moments & Equilibrium [QUANTUM ARITHMETIC]:
    │   └── Exact fixed-point reversible multipliers, adders, dividers in Q4.16
    │
    ├── 2. Non-Equilibrium Microstate Compression [QUANTUM STINESPRING]:
    │   └── Compressed environment: 14 non-equilibrium fields (224 qubits/node)
    │
    ├── 3. Spatial Streaming Permutation [QUANTUM]:
    │   └── Exact coordinate shift S (S^dag S = I)
    │
    └── 4. Wall Bounce-Back Involution [QUANTUM]:
        └── Exact reflection operator B (B^2 = I)
```

---

## 3. Classical & Hybrid Reference Baselines

1. `classical/level4_two_phase.py`: Pure classical floating-point Navier-Stokes & conservative phase-field LBM solver (Martin & Moyce benchmark).
2. `quantum/level6b_hybrid_solver.py`: Hybrid $K=1$ Local-Carleman physical baseline (**SHA-256 frozen reference**).
