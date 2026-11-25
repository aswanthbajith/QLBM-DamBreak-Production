"""Export cell-centred shallow-water fields for ParaView."""

from collections.abc import Sequence
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from numpy.typing import NDArray
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkCellDataToPointData
from vtkmodules.vtkIOXML import vtkXMLImageDataWriter

if __package__:
    from .shallow_water import velocity
else:
    from shallow_water import velocity


def with_display_depth(image: vtkImageData) -> vtkImageData:
    """Add an active point scalar for image viewers such as Kitware Glance."""
    converter = vtkCellDataToPointData()
    converter.SetInputData(image)
    converter.ProcessAllArraysOff()
    converter.AddCellDataArray("water_depth_m")
    converter.PassCellDataOn()
    converter.Update()

    result = converter.GetOutput()
    point_data = result.GetPointData()
    depth = vtk_to_numpy(point_data.GetArray("water_depth_m"))
    display_depth = numpy_to_vtk(depth.astype(np.float32), deep=True)
    display_depth.SetName("water_depth_display_m")
    point_data.RemoveArray("water_depth_m")
    point_data.SetScalars(display_depth)
    return result


def write_paraview(
    output: Path,
    times: Sequence[float],
    states: Sequence[NDArray],
    solid: NDArray,
    cell_size: float,
    gravity: float,
    density: float,
) -> None:
    """Write one VTI per state and a PVD collection with times in seconds."""
    directory = output / "paraview"
    directory.mkdir(parents=True, exist_ok=True)
    ny, nx = solid.shape
    wall_mask = solid.astype(np.uint8).ravel()
    area = cell_size**2
    document = ET.Element("VTKFile", type="Collection", version="0.1")
    collection = ET.SubElement(document, "Collection")

    for step, (time, state) in enumerate(zip(times, states, strict=True)):
        depth = state[0]
        u, v = velocity(state)
        vectors = np.stack((u, v, np.zeros_like(u)), axis=-1).reshape(-1, 3)
        fields = {
            "water_depth_m": depth.ravel(),
            "velocity_m_s": vectors,
            "speed_m_s": np.hypot(u, v).ravel(),
            "surface_elevation_m": depth.ravel(),  # Bed datum is zero.
            "bed_gauge_pressure_pa": (density * gravity * depth).ravel(),
            "water_mass_kg": (density * area * depth).ravel(),
            "solid": wall_mask,
        }

        image = vtkImageData()
        image.SetDimensions(nx + 1, ny + 1, 1)
        image.SetSpacing(cell_size, cell_size, 1.0)
        cell_data = image.GetCellData()
        # NumPy's C order has x varying fastest, as VTK expects.
        for name, values in fields.items():
            array = numpy_to_vtk(values, deep=True)
            array.SetName(name)
            cell_data.AddArray(array)
        cell_data.SetActiveScalars("water_depth_m")
        cell_data.SetActiveVectors("velocity_m_s")

        filename = f"step_{step:03d}.vti"
        writer = vtkXMLImageDataWriter()
        writer.SetFileName(str(directory / filename))
        writer.SetInputData(with_display_depth(image))
        if writer.Write() != 1:
            raise OSError(f"Could not write {directory / filename}.")
        ET.SubElement(
            collection, "DataSet", timestep=str(float(time)), part="0", file=filename
        )

    ET.indent(document)
    ET.ElementTree(document).write(
        directory / "flow.pvd", encoding="utf-8", xml_declaration=True
    )
