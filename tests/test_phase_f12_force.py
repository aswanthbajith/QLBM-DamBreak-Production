"""
Phase F12: Test Suite for Quantum Force & CSF Stencil Engine.
"""

import pytest
import numpy as np

from quantum.quantum_force import QuantumForceOracle


def test_quantum_force_oracle():
    """Verify force field calculation and stencil resource estimation."""
    force_oracle = QuantumForceOracle(nx=8, ny=4, g_acc=-0.0005, sigma=0.001)
    rho_field = np.ones((4, 8)) * 0.8
    alpha_field = np.zeros((4, 8))
    alpha_field[:, 0:4] = 1.0  # Sharp interface at x=3/4

    F_total, res_info = force_oracle.compute_force_fields(rho_field, alpha_field)

    assert F_total.shape == (2, 4, 8)
    assert res_info["shift_toffoli"] > 0
    assert res_info["shift_cx"] > 0
    # Interface normal force must be non-zero at interface zone
    assert abs(F_total[0, 1, 3]) > 0.0 or abs(F_total[0, 1, 2]) > 0.0
