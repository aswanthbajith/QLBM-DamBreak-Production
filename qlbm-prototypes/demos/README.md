# `qlbm` demos

This directory contains contains several examples of how users can use `qlbm` for simulating, visualizing, and analyzing QLBM algorithms. We recommend that each notebook is executed in a **python3.12** or **python3.13** virtual environment from this (`demos`) directory. You can create a new virtual environment as follows:

```bash
python -m venv qlbm-cpu-venv
source qlbm-cpu-venv/bin/activate
mkdir qlbm-output
pip install --upgrade pip
pip install -e ..[cpu,dev,docs]
pip install jupyter ipykernel seaborn pandas
jupyter lab
```

 Currently, the following directories are available:

## Visualization

Users can visualize both geometry and quantum circuits constructed from the JSON configurations. All quantum components (primitives, operators, algorithms) can be visually serialized to matplotlib, Latex, or text formats with the notebooks in the `visualization` directory.

## Simulation

`qlbm` currently supports two algorithms with different configurations and capabilities. To simulate the end-to-end algorithms and visualize the resulting flow field, users can interact with the notebooks in the `simulation` directory. Each notebook will generate outputs in a new `qlbm-output` directory. Each output subdirectory of `qlbm-output` will itself contain a `paraview` directory where the time step `step_<x>.vti` and geometry `cube_<x>.stl` files can be visualized in ParaView.

> **Note on visualization**: we rely on  ParaView for visualizing the flow field of the simulation. You can install ParaView from [this link](https://www.paraview.org/download/).

### Shallow-water dam breaks

From the repository root, run all ten layouts with the classical shallow-water model:

```bash
python -m demos.simulation.water_dam_break_cases
```

Pass a case ID such as `01-narrow-gate` to run one layout. Each case has a separate
folder under `demos/qlbm-output/water-dam-break-cases/`. Open `flow.gif` for a
depth map with velocity arrows, or `paraview/flow.pvd` for the time series of
cell-centred depth, velocity, speed, surface elevation, bed gauge pressure, and
water mass. `simulation.json` records the setup and water volume at each frame.

In Kitware Glance, open an individual `paraview/step_*.vti` and select
**Orientation Z** from the lower-left **3D** menu to display the 2D slice.
The active point field `water_depth_display_m` averages neighbouring cell depths
for display. Use `water_depth_m` and `velocity_m_s` in ParaView's Cell Data for
the simulation values. The GIF and the VTI series come from the same solver
snapshots.

The examples start with one metre of freshwater at rest on a flat, frictionless
bed, with dry ground downstream and the breach already open. The exterior and
solid walls reflect flow. The solver averages velocity over depth. The demo
requires NumPy, Matplotlib, Pillow, and VTK.

### 3D quantum fluid evolution

Run the single-phase shear-wave benchmark from the repository root:

```bash
python -m demos.simulation.quantum_fluid_evolution
```

The default run evolves a periodic 8 × 8 × 8 lattice through 12 timesteps with
Qiskit Aer. A 15-qubit circuit applies the linearized D3Q19 collision at full
relaxation and streams the populations along all three axes. The circuit retains
trajectories with a zero collision flag and continues evolving the accepted
fluid register. A separate NumPy implementation and an exact discrete shear
solution verify the results after circuit execution.

Open `demos/qlbm-output/quantum-fluid-3d/flow.gif` for the velocity animation or
`paraview/flow.pvd` in the same folder for all 3D snapshots. The velocity uses
lattice units, and relative density is the density divided by the resting
density. `simulation.json` records the postselection rate and verification
errors. The run uses statevector readout on a simulator and models small
perturbations of a single fluid on a periodic lattice. Gravity, solid walls,
and a moving water–air interface are additional dam-break physics.

### 3D quantum free-surface release

```bash
python -m demos.simulation.quantum_free_surface
```

This wet-bed narrow-gate case starts with a 0.16 m head difference in a 2 m × 2 m
tank. A harmonic potential on the 8 × 8 × 4 grid enforces zero normal velocity
at the dam, side walls, and bottom. A seven-qubit circuit evolves the surface
height and potential with gravity. Velocity throughout the water is recovered
from each circuit snapshot via the fixed harmonic extension. An independent
classical integration checks the results after the circuit has run.

Open `demos/qlbm-output/quantum-free-surface-3d/flow.gif` for the animation,
`paraview/surface.pvd` for the moving surface, and `paraview/flow.pvd` for the
three-component velocity on the reference water grid. `simulation.json` records
the numerical checks in SI units. The model assumes small, single-valued surface
displacements and constant atmospheric pressure, with both basins initially wet.

## Benchmarks

Users who are interested in developing and analyzing the theoretical and runtime properties of QLBMs can use the notebooks residing in the `benchmarks` directory. These notebooks contain utilities for automatically generating QLBM algorithms of different scales, logging relevant data about their properties, and parsing the data into helpful formats such as in-memory databases or plots. Benchmarks include simulator performance, statevector snapshot performance, and algorithm scalability with real hardware.
