"""Export a periodic 3D quantum shear-wave benchmark for viewing."""

from pathlib import Path
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from numpy.typing import NDArray
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter


def _write_paraview(
    directory: Path,
    velocities: NDArray,
    relative_density: NDArray,
    analytical_velocity: NDArray,
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    _, nz, ny, nx, _ = velocities.shape
    document = ET.Element("VTKFile", type="Collection", version="0.1")
    series = ET.SubElement(document, "Collection")

    for step, (velocity, density, reference) in enumerate(
        zip(velocities, relative_density, analytical_velocity, strict=True)
    ):
        image = vtkImageData()
        image.SetDimensions(nx, ny, nz)
        image.SetSpacing(1, 1, 1)
        fields = {
            # VTK point data is ordered with x varying fastest.
            "speed": np.linalg.norm(velocity, axis=-1).astype(np.float32).ravel(),
            "velocity": velocity.reshape(-1, 3),
            "relative_density": density.ravel(),
            "analytical_velocity": reference.reshape(-1, 3),
        }
        points = image.GetPointData()
        for name, values in fields.items():
            array = numpy_to_vtk(values, deep=True)
            array.SetName(name)
            points.AddArray(array)
        points.SetActiveScalars("speed")
        points.SetActiveVectors("velocity")

        name = f"step_{step:03d}.vti"
        writer = vtkXMLImageDataWriter()
        writer.SetFileName(str(directory / name))
        writer.SetInputData(image)
        if writer.Write() != 1:
            raise OSError(f"Could not write {directory / name}.")
        ET.SubElement(series, "DataSet", timestep=str(step), part="0", file=name)

    ET.indent(document)
    ET.ElementTree(document).write(
        directory / "flow.pvd", encoding="utf-8", xml_declaration=True
    )


def _write_animation(path: Path, velocities: NDArray, reference: NDArray) -> None:
    nt, nz, ny, nx, _ = velocities.shape
    times = np.arange(nt)
    speed = np.linalg.norm(velocities, axis=-1)
    rms = np.sqrt(np.mean(speed**2, axis=(1, 2, 3)))
    reference_rms = np.sqrt(np.mean(np.sum(reference**2, axis=-1), axis=(1, 2, 3)))

    # Use a fixed spatial sampling, color scale, and arrow scale across frames.
    stride = tuple((size + 3) // 4 for size in (nz, ny, nx))
    sample = tuple(slice(None, None, skip) for skip in stride)
    z, y, x = (axis[sample].ravel() for axis in np.indices((nz, ny, nx)))
    vectors = velocities[(slice(None), *sample)].reshape(nt, -1, 3)
    arrow_speed = np.linalg.norm(vectors, axis=-1)
    max_speed = float(speed.max()) or 1.0
    arrow_scale = 0.8 * min(stride) / max_speed
    color_scale = Normalize(0, max_speed)
    color_map = plt.get_cmap("viridis")

    figure = plt.figure(figsize=(9.4, 5.0), layout="constrained", facecolor="#f3f6fa")
    grid = figure.add_gridspec(1, 2, width_ratios=(1.45, 1))
    flow = figure.add_subplot(grid[0], projection="3d")
    decay = figure.add_subplot(grid[1])
    figure.suptitle("3D quantum fluid evolution", fontweight="bold", fontsize=16)
    flow.set_title("Velocity field · linearized D3Q19")
    flow.set(
        xlabel="x",
        ylabel="y",
        zlabel="z",
        xlim=(-1, nx),
        ylim=(-1, ny),
        zlim=(-1, nz),
        xticks=np.arange(0, nx, stride[2]),
        yticks=np.arange(0, ny, stride[1]),
        zticks=np.arange(0, nz, stride[0]),
    )
    flow.set_box_aspect((nx, ny, nz))
    flow.view_init(elev=24, azim=-55)
    flow.scatter(x, y, z, s=5, color="#526882", alpha=0.28, depthshade=False)
    figure.colorbar(
        ScalarMappable(norm=color_scale, cmap=color_map),
        ax=flow,
        shrink=0.65,
        pad=0.07,
        label="Speed (lattice units)",
    )

    decay.set_title("Shear-wave decay")
    decay.set(
        xlabel="Lattice time",
        ylabel="RMS speed (lattice units)",
        xlim=(-0.25, max(nt - 1, 1) + 0.25),
        ylim=(0, max(float(rms.max()), float(reference_rms.max()), 1e-15) * 1.12),
    )
    decay.xaxis.set_major_locator(MaxNLocator(integer=True))
    decay.grid(True, color="#d6e0eb", linewidth=0.7)
    decay.plot(
        times, reference_rms, linestyle="--", color="#6a7380", label="Analytical"
    )
    (line,) = decay.plot([], [], color="#155fa2", linewidth=2, label="Quantum circuit")
    (marker,) = decay.plot([], [], marker="o", color="#155fa2")
    decay.legend(loc="upper right")
    clock = flow.text2D(0.035, 0.95, "", transform=flow.transAxes, color="#233b55")
    arrows = None

    def draw(step: int) -> None:
        nonlocal arrows
        if arrows is not None:
            arrows.remove()
        colors = color_map(color_scale(arrow_speed[step]))
        arrows = flow.quiver(
            x,
            y,
            z,
            *vectors[step].T,
            length=arrow_scale,
            pivot="middle",
            linewidth=1.5,
            colors=np.tile(colors, (3, 1)),
        )
        line.set_data(times[: step + 1], rms[: step + 1])
        marker.set_data([step], [rms[step]])
        clock.set_text(f"Lattice time {step:d}")
        flow.set_xlim(-1, nx)
        flow.set_ylim(-1, ny)
        flow.set_zlim(-1, nz)

    try:
        animation = FuncAnimation(figure, draw, frames=nt, cache_frame_data=False)
        animation.save(path, writer=PillowWriter(fps=5), dpi=110)
    finally:
        plt.close(figure)


def write_outputs(
    output: Path,
    velocities: NDArray,
    relative_density: NDArray,
    analytical_velocity: NDArray,
) -> None:
    """Write circuit velocity snapshots and analytical diagnostics in lattice units.

    The array layout is (time, z, y, x, xyz) for velocity and (time, z, y, x)
    for density. Each periodic point occurs once, with no duplicated endpoint.
    """
    if velocities.ndim != 5 or velocities.shape[-1] != 3 or not velocities.shape[0]:
        raise ValueError("Expected velocities with shape (time, z, y, x, 3).")
    if min(velocities.shape[1:-1]) < 2:
        raise ValueError("Each spatial axis must contain at least two nodes.")
    if relative_density.shape != velocities.shape[:-1]:
        raise ValueError("Relative density must match the time and spatial grid.")
    if analytical_velocity.shape != velocities.shape:
        raise ValueError("Analytical velocity must match the circuit velocity fields.")
    if not all(
        np.isfinite(field).all()
        for field in (velocities, relative_density, analytical_velocity)
    ):
        raise ValueError("Flow fields must be finite.")

    _write_paraview(
        output / "paraview", velocities, relative_density, analytical_velocity
    )
    _write_animation(output / "flow.gif", velocities, analytical_velocity)
