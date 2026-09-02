"""
Phase F13: Test Suite for Coherent Velocity Generation & Limiter.
"""

import pytest
import numpy as np

from quantum.coherent_velocity import CoherentVelocityGenerator


def test_coherent_velocity_generation():
    """Verify shifted velocity calculation and low-Mach limiter."""
    vel_gen = CoherentVelocityGenerator(precision_format="Q4.12")
    rho_field = np.ones((4, 4)) * 0.8
    jx_field = np.ones((4, 4)) * 0.05
    jy_field = np.zeros((4, 4))
    Fx_field = np.zeros((4, 4))
    Fy_field = np.ones((4, 4)) * -0.0005

    u_field, costs = vel_gen.compute_coherent_velocity_fields(
        rho_field, jx_field, jy_field, Fx_field, Fy_field
    )

    assert u_field.shape == (2, 4, 4)
    u_mag = np.sqrt(u_field[0]**2 + u_field[1]**2)
    assert np.all(u_mag <= 0.15000001), "Mach limiter violated"
    assert costs["toffoli"] > 0
    assert costs["cx"] > 0
