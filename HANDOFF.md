# Handoff for review of the 3D quantum free-surface prototypes

## Review goal

Evaluate the mathematical formulation, circuit implementation, and validation of a narrow-gate water release. The long-term goal is a 3D dam break with quantum-circuit fluid evolution. The latest prototype advances a linearized moving water surface on simulated quantum gates. The review branch contains the full [QLBM prototype snapshot](qlbm-prototypes/) and its [generated results](qlbm-prototypes/demos/qlbm-output/). The host repository's existing 2D hybrid Carleman solver is a separate implementation.

## Current prototype

- The tank is 2 m × 2 m with 1 m mean water depth. The grid has 8 × 8 horizontal cells, four vertical layers, and 0.25 m spacing. A rigid interior wall runs across one column, with a 0.5 m opening at the center. The opening exists at the start of the simulation.
- Both basins start wet and at rest with a 0.16 m head difference. Gravity is 9.81 m/s². The model assumes inviscid, incompressible, irrotational water and constant atmospheric pressure. The surface is a single-valued height over the fixed water-domain planform.
- The spatial discretization solves Laplace's equation for velocity potential. It uses zero normal flux on solid faces and prescribed surface potential at the mean water level. The discrete Dirichlet-to-Neumann operator `G` maps surface potential `phi` to vertical velocity at that level. Its constant modes give the potential gauge.
- The evolution equations are `d(eta)/dt = G phi` and `d(phi)/dt = -g eta`. In energy coordinates `a = sqrt(g) eta` and `b = sqrt(G) phi`, the propagator is real orthogonal. For each eigenvalue `lambda` of `G`, the circuit update is the two-component rotation with rows `[cos(theta), sin(theta)]` and `[-sin(theta), cos(theta)]`, where `theta = sqrt(g lambda) dt`. Zero modes remain stationary. The inverse square root on positive modes decodes `phi` in a fixed gauge.
- Python assembles `G`, constructs the gate, and prepares the initial state once. Qiskit Aer applies the same unitary for every timestep and records statevector snapshots. The decoded surface potential is extended harmonically to obtain three-component water velocity. The classical reference integration checks the output after the circuit run and supplies no timestep feedback.

## Verified results

| Check | Result |
|---|---:|
| Quantum circuit and run | 7 qubits, 30 steps of 0.04 s, 31 snapshots through 1.2 s |
| Peak forward discharge through the breach | 0.2874 m³/s |
| Peak vertical cell-center velocity | 0.3230 m/s |
| Maximum water volume drift from the initial 3.625 m³ | 2.22 × 10⁻¹⁵ m³ |
| Maximum surface elevation error against an independent DOP853 integration of the same spatial model | 3.35 × 10⁻¹² m |
| Maximum discrete velocity divergence | 3.95 × 10⁻¹⁴ s⁻¹ |

Additional checks verified exactly zero normal velocity on impermeable faces, agreement between breach discharge and the downstream rate of volume change, and a motionless solution when the gate was sealed. A rectangular-tank cosine mode showed second-order spatial convergence toward the finite-depth dispersion relation. The DOP853 comparison verifies circuit time evolution for the discrete equations. Physical validation of the release against an experiment is pending.

## Related experiments and reproduction

Run these commands from the repository root with Qiskit 2.1.0, Qiskit Aer 0.17.2, NumPy, SciPy, Matplotlib, Pillow, and VTK installed.

```sh
cd qlbm-prototypes
python -m demos.simulation.quantum_fluid_evolution
python -m demos.simulation.quantum_free_surface
```

- [`quantum_fluid_evolution.py`](qlbm-prototypes/demos/simulation/quantum_fluid_evolution.py) and its reference and output modules implement a periodic 8 × 8 × 8 D3Q19 shear-wave benchmark. Its 15-qubit circuit implements linearized full-relaxation BGK collision via postselection and periodic streaming via controlled shifts. Twelve steps matched the exact discrete velocity within 5.85 × 10⁻¹³ lattice units. Fourteen of 128 simulated shots survived all collisions.
- [`quantum_free_surface.py`](qlbm-prototypes/demos/simulation/quantum_free_surface.py) assembles and runs the free-surface circuit. [`quantum_free_surface_model.py`](qlbm-prototypes/demos/simulation/quantum_free_surface_model.py) supplies the spatial model and [`quantum_free_surface_output.py`](qlbm-prototypes/demos/simulation/quantum_free_surface_output.py) writes the GIF and VTK data. In `demos/qlbm-output/quantum-free-surface-3d/`, `flow.gif` shows the moving interface, `paraview/surface.pvd` animates the surface, and `paraview/flow.pvd` shows the reference-grid velocity. `simulation.json` holds the run diagnostics. [Free-surface results](qlbm-prototypes/demos/qlbm-output/quantum-free-surface-3d/) · [D3Q19 benchmark results](qlbm-prototypes/demos/qlbm-output/quantum-fluid-3d/)
- The earlier OpenFOAM 3D narrow-gate result is a classical water–air CFD comparison. The ten other water-depth and velocity cases use a classical depth-averaged shallow-water solver.

## Questions for the reviewer

1. Check the sign, units, gauge, and energy normalization of the Dirichlet-to-Neumann map and its quantum propagator. Check the zero-flux geometry and volume balance across the gate.
2. Separate verification of gate evolution from validation of fluid physics. Identify convergence checks beyond the existing dispersion test, and propose comparisons for surface elevation, arrival time, and gate discharge.
3. Assess gate synthesis, amplitude preparation, and phase-sensitive readout costs for a larger lattice. The evidence here comes from full-state simulator readout. A hardware feasibility or speedup claim would need separate evidence.
4. Propose a staged route to a nonlinear 3D release with wetting and drying, overturning or disconnected water surfaces, and explicit air dynamics where needed. State which updates would run in circuits, which operations would run classically, and what evidence would distinguish a new verified result from a proposal.

Background for the surface equations and a later experimental comparison are available in the [linear water-wave formulation](https://doi.org/10.1007/s42286-024-00107-0) and [MARIN 3D dam-break benchmark](https://www.spheric-sph.org/tests/test-02).
