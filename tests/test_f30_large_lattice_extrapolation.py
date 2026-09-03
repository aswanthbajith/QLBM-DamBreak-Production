"""
Phase F30: Test Suite for Large-Lattice Analytical Extrapolations.
"""

import pytest
from quantum.f30_scaling_engine import F30ScalingEngine


def test_large_lattice_extrapolations():
    """Verify resource scaling up to 128x64 engineering grid."""
    extrap = F30ScalingEngine.get_large_lattice_extrapolations(bit_width=16)

    assert len(extrap) == 7
    grid_128x64 = [e for e in extrap if e["grid"] == "128x64"][0]
    assert grid_128x64["nodes"] == 8192
    assert grid_128x64["status"] == "EXTRAPOLATED"
    assert grid_128x64["total_logical_qubits"] == 8192 * 18 * 16 * 2 + 48  # 4,718,640
