# FINAL PROJECT TREE & FILE CLASSIFICATION
## Complete Classification of All Tracked Source Files

---

## 1. Directory Tree & Categorization

```text
QLBM-DamBreak-Production/
├── classical/
│   ├── d2q9.py                           [ACTIVE / CORE PHYSICS]
│   ├── level4_two_phase.py               [ACTIVE / GROUND TRUTH REFERENCE]
│   ├── equilibrium.py                    [ACTIVE / NUMERICAL UTILITY]
│   ├── streaming.py                      [ACTIVE / CLASSICAL REFERENCE]
│   ├── boundary.py                       [ACTIVE / CLASSICAL REFERENCE]
│   └── reference_solver.py               [REFERENCE / BASELINE ENGINE]
│
├── quantum/
│   ├── level6b_hybrid_solver.py          [FROZEN REFERENCE / SHA-256 VERIFIED]
│   ├── f38_qpu_executor.py               [ACTIVE / PRIMARY EXECUTION ENGINE]
│   ├── f38_backend_discovery.py          [ACTIVE / HARDWARE DISCOVERY]
│   ├── f38_observables_reconstruction.py [ACTIVE / READOUT DECODER]
│   ├── f38_multi_layer_validator.py      [ACTIVE / VALIDATOR ENGINE]
│   ├── f33_hardware_demo.py              [ACTIVE / PRIMARY NISQ DEMONSTRATOR]
│   ├── f33_state_preparation.py          [ACTIVE / QUANTUM STATE PREP]
│   ├── f31_reduced_architecture.py       [ACTIVE / SCALABLE FTQC CIRCUIT]
│   ├── f29_scalable_circuit.py           [ACTIVE / SCALABLE FTQC CIRCUIT]
│   ├── f27_local_node_circuit.py         [ACTIVE / REVERSIBLE ARITHMETIC]
│   ├── f22_stinespring.py                [ACTIVE / CPTP CHANNEL ENGINE]
│   ├── streaming.py                      [ACTIVE / QUANTUM SWAP STREAMING]
│   ├── physical_boundary_mask.py         [ACTIVE / QUANTUM BOUNCE-BACK]
│   ├── f17_reversible_collision.py       [EXPERIMENTAL / FIXED-POINT LOGIC]
│   ├── f15_carleman_collision.py         [REJECTED / TRUNCATION FAILURE ARTIFACT]
│   └── level6_lifted_carleman.py         [REJECTED / DILATION LEAKAGE ARTIFACT]
│
├── scripts/
│   ├── run_phase_f38_validation.py       [ACTIVE / MASTER VALIDATION ENTRYPOINT]
│   ├── run_phase_f38_ideal.py            [ACTIVE / IDEAL SIMULATOR ENTRYPOINT]
│   ├── run_phase_f38_noisy.py            [ACTIVE / NOISY HARDWARE EMULATION]
│   ├── run_phase_f38_dryrun.py           [ACTIVE / HARDWARE TRANSPILATION AUDIT]
│   ├── run_phase_f38_qpu.py              [ACTIVE / GUARDED QPU SUBMISSION GATE]
│   ├── run_phase_f31_reduction.py        [ACTIVE / FTQC COMPRESSION AUDIT]
│   ├── run_phase_f29_validation.py       [ACTIVE / FTQC SCALABLE VALIDATOR]
│   └── ... (Historical run scripts)     [ARCHIVE / REPRODUCIBILITY ASSETS]
│
├── tests/
│   ├── test_final_integrated_prototype.py [ACTIVE / MASTER INTEGRATION TEST]
│   ├── test_f38_*.py                     [ACTIVE / HARDWARE & VALIDATION TESTS]
│   ├── test_f31_*.py                     [ACTIVE / RESOURCE REDUCTION TESTS]
│   ├── test_f29_*.py                     [ACTIVE / SCALABLE CIRCUIT TESTS]
│   ├── test_f18_*.py                     [ACTIVE / NON-INJECTIVITY PROOF TESTS]
│   ├── test_f15_*.py                     [ACTIVE / CARLEMAN BREAKDOWN TESTS]
│   ├── test_level6b_*.py                 [ACTIVE / FROZEN BASELINE TESTS]
│   └── test_level4_*.py                  [ACTIVE / CLASSICAL GROUND TRUTH TESTS]
│
├── docs/                                 [DOCUMENTATION / FORENSIC ARCHIVE]
└── results/                              [DATA / AUDIT MATRICES & PROVENANCE]
```

### Preservation Guarantee:
Zero historical files, rejected architectures, or research diaries were deleted. Every historical investigation remains intact and executable.
