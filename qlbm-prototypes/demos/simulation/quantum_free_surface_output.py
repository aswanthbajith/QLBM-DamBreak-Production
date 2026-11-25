"""Visualize the quantum free-surface benchmark in physical units."""

from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numpy.typing import NDArray
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkImageData, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkCellDataToPointData
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter, vtkXMLPolyDataWriter


def _surface_topology(wet: NDArray, spacing: float):
    """Triangulate each wet square using its centre and four shared corners."""
    _, nx = wet.shape
    y, x = np.nonzero(wet)
    corners = y * (nx + 1) + x
    corner_ids, faces = np.unique(
        np.stack([corners, corners + 1, corners + nx + 2, corners + nx + 1], axis=1),
        return_inverse=True,
    )
    faces = faces.reshape(-1, 4)
    corner_xy = np.stack([corner_ids % (nx + 1), corner_ids // (nx + 1)], axis=1)
    center_xy = np.stack([x + 0.5, y + 0.5], axis=1)
    xy = np.concatenate([corner_xy, center_xy]) * spacing
    centers = np.broadcast_to(
        (len(corner_ids) + np.arange(len(x)))[:, None], faces.shape
    )
    triangles = np.stack([centers, faces, np.roll(faces, -1, axis=1)], axis=-1)
    return xy, faces, triangles.reshape(-1, 3)


def _surface_points(height: NDArray, xy: NDArray, faces: NDArray) -> NDArray:
    # Height at every column centre is the exact field. Shared corners use
    # averages for display between centres, even along the dam walls.
    connectivity = faces.ravel()
    corner_height = np.bincount(
        connectivity, weights=np.repeat(height, 4)
    ) / np.bincount(connectivity)
    return np.column_stack((xy, np.concatenate([corner_height, height])))


def _array(name: str, values: NDArray):
    result = numpy_to_vtk(values, deep=True)
    result.SetName(name)
    return result


def _write_pvd(path: Path, entries) -> None:
    document = ET.Element("VTKFile", type="Collection", version="0.1")
    series = ET.SubElement(document, "Collection")
    for time, filename in entries:
        ET.SubElement(series, "DataSet", timestep=str(float(time)), part="0", file=filename)
    ET.indent(document)
    ET.ElementTree(document).write(path, encoding="utf-8", xml_declaration=True)


def _write_paraview(
    output: Path,
    points_by_frame: NDArray,
    triangles: NDArray,
    elevations: NDArray,
    velocities: NDArray,
    wet: NDArray,
    spacing: float,
    times: NDArray,
) -> None:
    directory = output / "paraview"
    directory.mkdir(parents=True, exist_ok=True)
    _, nz, ny, nx, _ = velocities.shape
    polygons = vtkCellArray()
    polygons.SetData(
        numpy_to_vtkIdTypeArray(np.arange(0, triangles.size + 1, 3), deep=True),
        numpy_to_vtkIdTypeArray(triangles.ravel(), deep=True),
    )
    columns = np.broadcast_to(wet, (nz, ny, nx))
    flow_entries = []
    surface_entries = []
    for index, (points, heights, velocity, time) in enumerate(
        zip(points_by_frame, elevations, velocities, times, strict=True)
    ):
        image = vtkImageData()
        image.SetDimensions(nx + 1, ny + 1, nz + 1)
        image.SetSpacing(spacing, spacing, spacing)
        data = image.GetCellData()
        data.SetVectors(_array("velocity_m_s", velocity.reshape(-1, 3)))
        speed = np.linalg.norm(velocity, axis=-1).astype(np.float32)
        data.SetScalars(_array("speed_m_s", speed.ravel()))
        data.AddArray(_array("water_column", columns.astype(np.uint8).ravel()))
        column_elevations = np.broadcast_to(np.where(wet, heights, 0.0), columns.shape)
        data.AddArray(_array("surface_elevation_m", column_elevations.ravel()))

        # Preserve cell centres for analysis and provide point speed for image
        # viewers such as Glance that need an active point scalar.
        converter = vtkCellDataToPointData()
        converter.SetInputData(image)
        converter.ProcessAllArraysOff()
        converter.AddCellDataArray("speed_m_s")
        converter.PassCellDataOn()
        converter.Update()
        point_data = converter.GetOutput().GetPointData()
        point_data.GetArray("speed_m_s").SetName("speed_display_m_s")
        point_data.SetActiveScalars("speed_display_m_s")
        flow_filename = f"flow_{index:03d}.vti"
        writer = vtkXMLImageDataWriter()
        writer.SetFileName(str(directory / flow_filename))
        writer.SetInputConnection(converter.GetOutputPort())
        if writer.Write() != 1:
            raise OSError(f"Could not write {directory / flow_filename}.")
        flow_entries.append((time, flow_filename))

        surface = vtkPolyData()
        vertices = vtkPoints()
        vertices.SetData(numpy_to_vtk(points, deep=True))
        surface.SetPoints(vertices)
        surface.SetPolys(polygons)
        surface.GetPointData().SetScalars(_array("elevation_m", points[:, 2]))
        surface.GetCellData().AddArray(
            _array("column_center_elevation_m", np.repeat(heights[wet], 4))
        )
        surface_filename = f"surface_{index:03d}.vtp"
        writer = vtkXMLPolyDataWriter()
        writer.SetFileName(str(directory / surface_filename))
        writer.SetInputData(surface)
        if writer.Write() != 1:
            raise OSError(f"Could not write {directory / surface_filename}.")
        surface_entries.append((time, surface_filename))

    _write_pvd(directory / "flow.pvd", flow_entries)
    _write_pvd(directory / "surface.pvd", surface_entries)
    copyfile(directory / surface_entries[-1][1], output / "water-surface.vtp")


def _write_animation(
    path: Path,
    points_by_frame: NDArray,
    triangles: NDArray,
    elevations: NDArray,
    velocities: NDArray,
    wet: NDArray,
    spacing: float,
    times: NDArray,
) -> None:
    _, nz, ny, nx, _ = velocities.shape
    depth = nz * spacing
    wall_height = depth * 1.25
    width, length = nx * spacing, ny * spacing
    displacement = (elevations - depth) * 100
    limit = max(float(np.max(np.abs(displacement[:, wet]))), 0.1)
    norm = Normalize(vmin=-limit, vmax=limit)
    palette = LinearSegmentedColormap.from_list(
        "free-surface", ("#874325", "#e0a667", "#edf7ff", "#54b4d1", "#073e78")
    )
    palette.set_bad("#343e4f")

    fig = plt.figure(figsize=(11.2, 6.2), layout="constrained")
    grid = fig.add_gridspec(1, 2, width_ratios=(1.12, 1))
    ax = fig.add_subplot(grid[0], projection="3d")
    top = fig.add_subplot(grid[1])
    fig.patch.set_facecolor("#f5f8fb")
    fig.suptitle("Quantum free-surface flow through a breach", fontweight="bold", fontsize=17)

    wall_y, wall_x = np.nonzero(~wet)
    if wall_x.size:
        ax.bar3d(
            wall_x * spacing, wall_y * spacing, np.zeros(len(wall_x)),
            spacing, spacing, wall_height, color="#4b5566", edgecolor="none",
        )
    ax.set_title("Moving water surface")
    ax.set(
        xlim=(0, width), ylim=(0, length), zlim=(0, max(wall_height, elevations[:, wet].max())),
        xlabel="x (m)", ylabel="y (m)", zlabel="Elevation (m)",
    )
    ax.set_proj_type("ortho")
    ax.set_box_aspect((width, length, wall_height))
    ax.view_init(elev=31, azim=-51)
    surface = Poly3DCollection(
        points_by_frame[0][triangles], linewidth=0, antialiaseds=False,
    )
    ax.add_collection3d(surface)

    top.set_title("Surface displacement and flow")
    top.set(xlabel="x (m)", ylabel="y (m)")
    image = top.imshow(
        np.ma.array(displacement[0], mask=~wet), origin="lower",
        extent=(0, width, 0, length), cmap=palette, norm=norm, interpolation="nearest",
    )
    horizontal = velocities[..., :2].mean(axis=1)
    max_speed = float(np.linalg.norm(horizontal[:, wet], axis=-1).max())
    quiver_scale = max(max_speed, 1e-12) / (0.7 * spacing)
    y, x = np.nonzero(wet)
    arrows = top.quiver(
        (x + 0.5) * spacing, (y + 0.5) * spacing, *horizontal[0, wet].T,
        color="#16253a", edgecolor="white", linewidth=0.25,
        angles="xy", scale_units="xy", scale=quiver_scale, minlength=0,
    )
    if max_speed > 1e-12:
        reference_speed = float(f"{0.7 * max_speed:.1g}")
        top.quiverkey(
            arrows, 0.05, -0.18, reference_speed, f"{reference_speed:g} m/s",
            labelpos="E",
        )
    clock = top.text(
        1, -0.17, "", ha="right", va="top", transform=top.transAxes,
        color="#243a58", fontsize=10,
    )
    fig.colorbar(
        ScalarMappable(norm=norm, cmap=palette), ax=(ax, top), location="bottom",
        fraction=0.065, shrink=0.77, label=f"Surface displacement from {depth:g} m (cm)",
    )
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis, top.xaxis, top.yaxis):
        axis.set_major_locator(MaxNLocator(5))

    def draw(index: int) -> None:
        surface.set_verts(points_by_frame[index][triangles])
        surface.set_facecolor(palette(norm(np.repeat(displacement[index, wet], 4))))
        image.set_data(np.ma.array(displacement[index], mask=~wet))
        arrows.set_UVC(*horizontal[index, wet].T)
        clock.set_text(f"Time {times[index]:.2f} s")

    try:
        animation = FuncAnimation(fig, draw, frames=len(times), cache_frame_data=False)
        animation.save(path, writer=PillowWriter(fps=10), dpi=110)
    finally:
        plt.close(fig)


def write_outputs(
    output: Path,
    elevations: NDArray,
    velocities: NDArray,
    wet: NDArray,
    spacing: float,
    times: NDArray,
) -> None:
    """Write the moving surface and velocities on the fixed reference mesh.

    The xyz velocity components are in m/s. The surface heights, mesh spacing,
    and physical coordinates are in metres. Solid wall cells carry no surface.
    """
    if elevations.ndim != 3 or velocities.ndim != 5 or velocities.shape[-1] != 3:
        raise ValueError("Expected elevation (time,y,x) and velocity (time,z,y,x,3).")
    if elevations.shape != (velocities.shape[0], *velocities.shape[2:4]):
        raise ValueError("Surface and velocity grids must have matching times and columns.")
    if wet.shape != elevations.shape[1:] or wet.dtype != np.bool_ or not wet.any():
        raise ValueError("Wet columns must be a nonempty Boolean mask of the surface grid.")
    if not np.isfinite(spacing) or spacing <= 0:
        raise ValueError("Grid spacing must be finite and positive.")
    if times.shape != elevations.shape[:1] or not len(times) or not np.isfinite(times).all():
        raise ValueError("Expected one finite time for each frame.")
    if not np.isfinite(elevations[:, wet]).all() or not np.isfinite(velocities).all():
        raise ValueError("Surface heights and velocities must be finite.")

    xy, faces, triangles = _surface_topology(wet, spacing)
    points = np.stack([_surface_points(height[wet], xy, faces) for height in elevations])
    _write_paraview(output, points, triangles, elevations, velocities, wet, spacing, times)
    _write_animation(
        output / "flow.gif", points, triangles, elevations, velocities, wet, spacing, times
    )
