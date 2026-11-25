"""Run ten collisionless D2Q9 dam releases and export their animations."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle
from qiskit_aer import AerSimulator
from vtk import vtkXMLImageDataReader
from vtk.util.numpy_support import vtk_to_numpy

from qlbm.components import (
    ABDiscreteUniformInitialConditions,
    ABGridMeasurement,
    CQLBM,
    EmptyPrimitive,
)
from qlbm.infra import QiskitRunner, SimulationConfig
from qlbm.lattice import ABLattice

if __package__:
    from .dam_break_layouts import CASES, SIZE
else:
    from dam_break_layouts import CASES, SIZE

SHOTS = 4096
STEPS = 8


def simulate(output, reservoir, velocities, walls):
    x, y, width, height = reservoir
    lattice = ABLattice({
        "lattice": {"dim": {"x": SIZE, "y": SIZE}, "velocities": "d2q9"},
        "geometry": [
            {"shape": "cuboid", "x": [x0, x1], "y": [y0, y1], "boundary": "bounceback"}
            for x0, x1, y0, y1 in walls
        ],
    })
    initial = ABDiscreteUniformInitialConditions(
        lattice, list(velocities),
        (list(range(width.bit_length() - 1)), list(range(height.bit_length() - 1))),
    ).circuit
    for axis, origin in enumerate((x, y)):
        for bit, qubit in enumerate(lattice.grid_index(axis)):
            if origin & (1 << bit):
                initial.x(qubit)

    config = SimulationConfig(
        initial_conditions=initial,
        algorithm=CQLBM(lattice),
        postprocessing=EmptyPrimitive(lattice),
        measurement=ABGridMeasurement(lattice),
        target_platform="QISKIT",
        compiler_platform="QISKIT",
        optimization_level=0,
        statevector_sampling=True,
        execution_backend=AerSimulator(method="statevector", max_parallel_threads=2),
        sampling_backend=AerSimulator(
            method="statevector", max_parallel_threads=2, seed_simulator=42,
        ),
    )
    config.prepare_for_simulation()
    QiskitRunner(config, lattice).run(
        STEPS, SHOTS, str(output), statevector_snapshots=True,
    )


def animate(output, title, walls):
    frames = []
    for step in range(STEPS + 1):
        reader = vtkXMLImageDataReader()
        reader.SetFileName(str(output / "paraview" / f"step_{step:03d}.vti"))
        reader.Update()
        counts = vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars())
        frames.append(counts.reshape(SIZE, SIZE) / SHOTS)

    fig, ax = plt.subplots(figsize=(6, 5), layout="constrained")
    image = ax.imshow(
        frames[0], origin="lower", cmap="Blues", interpolation="nearest",
        vmin=0, vmax=max(frame.max() for frame in frames),
    )
    for x0, x1, y0, y1 in walls:
        ax.add_patch(Rectangle(
            (x0 - 0.5, y0 - 0.5), x1 - x0 + 1, y1 - y0 + 1,
            facecolor="#4b5563", edgecolor="#1f2937",
        ))
    ax.set(xlabel="x", ylabel="y", xticks=range(0, SIZE, 3), yticks=range(0, SIZE, 3))
    fig.colorbar(image, ax=ax, label="Measured position probability")

    def draw(step):
        image.set_data(frames[step])
        ax.set_title(f"{title} · step {step:02d}")

    animation = FuncAnimation(fig, draw, frames=len(frames))
    animation.save(output / "flow.gif", writer=PillowWriter(fps=2), dpi=120)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="*", metavar="CASE", help="Case IDs. Default: all.")
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "qlbm-output" / "dam-break-cases",
    )
    args = parser.parse_args()
    for name in args.cases or CASES:
        if name not in CASES:
            parser.error(f"Unknown case {name}. Choose from {', '.join(CASES)}.")
        title, reservoir, velocities, walls = CASES[name]
        output = args.output / name
        print(f"Running {name}", flush=True)
        simulate(output, reservoir, velocities, walls)
        animate(output, title, walls)


if __name__ == "__main__":
    main()
