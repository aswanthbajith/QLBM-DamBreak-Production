"""
Phase F13: Test Suite for Coherent Force & CSF Generator.
"""

import pytest
import numpy as np

from quantum.coherent_force import CoherentForceGenerator


def test_coherent_force_generation():
    """Verify buoyancy and CSF calculation."""
    force_gen = CoherentForceGenerator(nx=8, ny=4, g_acc=-0.0005, sigma=0.001)
    rho_field = np.ones((4, 8)) * 0.8
    alpha_field = np.zeros((4, 8))
    alpha_field[:, 0:4] = 1.0

    F_field, costs = force_gen.compute_coherent_force_fields(rho_field, alpha_field)

    assert F_field.shape == (2, 4, 8)
    assert costs["toffoli"] > 0
    assert abs(F_field[1, 0, 0]) > 0.0  # Buoyancy active
