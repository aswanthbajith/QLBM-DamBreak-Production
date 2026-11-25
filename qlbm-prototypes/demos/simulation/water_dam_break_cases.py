"""Run the ten dam-break layouts with gravity-driven shallow-water flow."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch, Rectangle

if __package__:
    from .dam_break_layouts import CASES, SIZE
    from .shallow_water import simulate, velocity
    from .shallow_water_output import write_paraview
else:
    from dam_break_layouts import CASES, SIZE
    from shallow_water import simulate, velocity
    from shallow_water_output import write_paraview

CELLS_PER_METRE = 4
CELL_SIZE_M = 1 / CELLS_PER_METRE
RESERVOIR_DEPTH_M = 1.0
GRAVITY_M_S2 = 9.81
WATER_DENSITY_KG_M3 = 1000.0
DURATION_S = 5.0
FRAME_INTERVAL_S = 0.125

# Bounds in metres, as (x_min, x_max, y_min, y_max).
# The reservoir starts at rest and touches the upstream face of the dam.
RESERVOIRS = {
    "01-narrow-gate": (0, 9, 0, SIZE),
    "02-full-collapse": (0, 6, 0, SIZE),
    "03-side-breach": (0, 9, 0, SIZE),
    "04-twin-breaches": (0, 9, 0, SIZE),
    "05-northbound-release": (0, SIZE, 0, 9),
    "06-southbound-release": (0, SIZE, 7, SIZE),
    "07-staggered-dams": (0, 8, 0, SIZE),
    "08-island-split": (0, 8, 0, SIZE),
    "09-narrow-canal": (0, 8, 0, SIZE),
    "10-offset-outlet": (0, 8, 0, SIZE),
}


def initial_conditions(name):
    title, _, _, quantum_walls = CASES[name]
    walls = [(x0, x1 + 1, y0, y1 + 1) for x0, x1, y0, y1 in quantum_walls]
    if name == "10-offset-outlet":
        # Extend the downstream wall to the top edge, leaving one outlet.
        walls[-1] = (12, 14, 5, SIZE)

    shape = (SIZE * CELLS_PER_METRE, SIZE * CELLS_PER_METRE)
    solid = np.zeros(shape, dtype=bool)
    for x0, x1, y0, y1 in walls:
        solid[
            y0 * CELLS_PER_METRE : y1 * CELLS_PER_METRE,
            x0 * CELLS_PER_METRE : x1 * CELLS_PER_METRE,
        ] = True

    x0, x1, y0, y1 = RESERVOIRS[name]
    depth = np.zeros(shape)
    depth[
        y0 * CELLS_PER_METRE : y1 * CELLS_PER_METRE,
        x0 * CELLS_PER_METRE : x1 * CELLS_PER_METRE,
    ] = RESERVOIR_DEPTH_M
    return title, walls, depth, solid


def animate(path, title, walls, times, states):
    fig, ax = plt.subplots(figsize=(7.2, 6), layout="constrained")
    fig.patch.set_facecolor("#faf9f7")
    ax.set_facecolor("#eee8db")
    colormap = LinearSegmentedColormap.from_list(
        "water", ("#aadfeb", "#2696c2", "#07366e")
    )
    colormap.set_bad(alpha=0)
    vmax = max(RESERVOIR_DEPTH_M, max(float(state[0].max()) for state in states))
    image = ax.imshow(
        np.ma.masked_less(states[0][0], 0.005),
        origin="lower",
        extent=(0, SIZE, 0, SIZE),
        interpolation="nearest",
        cmap=colormap,
        vmin=0,
        vmax=vmax,
    )
    for x0, x1, y0, y1 in walls:
        ax.add_patch(
            Rectangle(
                (x0, y0), x1 - x0, y1 - y0, facecolor="#394555",
                edgecolor="#263241", linewidth=0.7,
            )
        )

    coords = (np.arange(states[0].shape[-1]) + 0.5) * CELL_SIZE_M
    sample = np.s_[2::4, 2::4]
    xv, yv = np.meshgrid(coords[2::4], coords[2::4])
    arrows = ax.quiver(
        xv, yv, np.zeros_like(xv), np.zeros_like(yv),
        color="#fff5d4", edgecolor="#14273d", linewidth=0.35, width=0.006,
        angles="xy", scale_units="xy", scale=3.0, minlength=0,
    )
    ax.quiverkey(arrows, 0.01, 1.025, 2, "2 m/s", labelpos="E", color="#394555")
    if walls:
        ax.legend(handles=[Patch(color="#394555", label="Solid wall")], loc="upper left")
    ax.set(
        xlabel="x (m)", ylabel="y (m)",
        xticks=np.arange(0, SIZE + 1, 4), yticks=np.arange(0, SIZE + 1, 4),
    )
    fig.colorbar(image, ax=ax, label="Water depth (m)", shrink=0.88)
    fig.suptitle(title, fontsize=14, fontweight="bold")
    clock = ax.set_title("", loc="right", fontsize=10)

    def draw(frame):
        state = states[frame]
        depth = state[0]
        image.set_data(np.ma.masked_less(depth, 0.005))
        u, v = velocity(state)
        hide = (depth[sample] < 0.02) | (np.hypot(u[sample], v[sample]) < 0.15)
        arrows.set_UVC(
            np.ma.array(u[sample], mask=hide), np.ma.array(v[sample], mask=hide)
        )
        clock.set_text(f"Time {times[frame]:.2f} s")

    animation = FuncAnimation(fig, draw, frames=len(times), cache_frame_data=False)
    animation.save(path, writer=PillowWriter(fps=1 / FRAME_INTERVAL_S), dpi=110)
    plt.close(fig)


def run_case(output, name):
    title, walls, depth, solid = initial_conditions(name)
    times = np.linspace(0, DURATION_S, round(DURATION_S / FRAME_INTERVAL_S) + 1)
    states = list(simulate(depth, solid, CELL_SIZE_M, times, GRAVITY_M_S2))
    output.mkdir(parents=True, exist_ok=True)
    write_paraview(
        output, times, states, solid, CELL_SIZE_M, GRAVITY_M_S2, WATER_DENSITY_KG_M3
    )
    animate(output / "flow.gif", title, walls, times, states)
    volumes = [float(state[0].sum()) * CELL_SIZE_M**2 for state in states]
    metadata = {
        "case": title,
        "model": "Classical 2D shallow-water equations on a flat, frictionless bed",
        "boundary": "Reflecting solid walls and exterior boundaries",
        "breach": "Open at t = 0",
        "cell_size_m": CELL_SIZE_M,
        "gravity_m_s2": GRAVITY_M_S2,
        "water_density_kg_m3": WATER_DENSITY_KG_M3,
        "initial_reservoir_depth_m": RESERVOIR_DEPTH_M,
        "initial_reservoir_bounds_m": RESERVOIRS[name],
        "wall_bounds_m": walls,
        "output_times_s": times.tolist(),
        "volume_m3": volumes,
        "maximum_absolute_volume_error_m3": max(abs(vol - volumes[0]) for vol in volumes),
    }
    (output / "simulation.json").write_text(json.dumps(metadata, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="*", metavar="CASE", help="Case IDs. Default: all.")
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "qlbm-output" / "water-dam-break-cases",
    )
    args = parser.parse_args()
    names = args.cases or CASES
    for name in names:
        if name not in CASES:
            parser.error(f"Unknown case {name}. Choose from {', '.join(CASES)}.")
    for name in names:
        print(f"Running {name}", flush=True)
        run_case(args.output / name, name)


if __name__ == "__main__":
    main()
