"""
Phase F22: Test Suite for Exact Zeroth-Moment Mass Conservation in BGK Collision.
"""

import pytest
import numpy as np

from quantum.f22_mass_conservation import F22ExactMassConservingBGKEngine


def test_exact_integer_mass_conservation():
    """Verify sum f_out == sum f_in == rho_in strictly to exact integer precision."""
    engine = F22ExactMassConservingBGKEngine(omega_f=1.2, omega_g=1.4)

    # Arbitrary non-equilibrium distribution
    f_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    g_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]

    f_out, g_out, meta = engine.evaluate_conservative_bgk_map(f_in, g_in, F_ext=(10, -5))

    assert meta["is_mass_conserved"] == True
    assert meta["is_phase_conserved"] == True
    assert sum(f_out) == sum(f_in)
    assert sum(g_out) == sum(g_in)
