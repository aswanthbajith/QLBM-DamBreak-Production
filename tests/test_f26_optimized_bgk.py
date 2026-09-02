"""
Phase F26: Test Suite for Symmetry-Optimized BGK Engine.
"""

import pytest
import numpy as np

from quantum.f22_mass_conservation import F22ExactMassConservingBGKEngine
from quantum.f26_optimized_bgk import F26OptimizedBGKEngine


def test_optimized_bgk_exact_equivalence():
    """Verify that symmetry-optimized BGK produces 100% identical outputs to F22 engine."""
    f22_eng = F22ExactMassConservingBGKEngine(omega_f=1.1, omega_g=1.3)
    f26_eng = F26OptimizedBGKEngine(omega_f=1.1, omega_g=1.3)

    f_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    g_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    f_ext = (14, -8)

    f_out_22, g_out_22, meta_22 = f22_eng.evaluate_conservative_bgk_map(f_in, g_in, F_ext=f_ext)
    f_out_26, g_out_26, meta_26 = f26_eng.evaluate_optimized_bgk_map(f_in, g_in, F_ext=f_ext)

    assert f_out_22 == f_out_26
    assert g_out_22 == g_out_26
    assert meta_26["is_mass_conserved"] == True
    assert meta_26["is_phase_conserved"] == True
