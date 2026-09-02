"""
Phase F24: Test Suite for Momentum Invariance under Rest-Particle Residual Absorption.
"""

import pytest
from quantum.f24_momentum_audit import F24MomentumForensicAudit


def test_rest_particle_momentum_invariance():
    """Verify that rest particle f0 absorption has zero effect on fluid momentum."""
    f_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]
    g_in = [1800, 450, 450, 450, 450, 110, 110, 110, 110]

    audit = F24MomentumForensicAudit.audit_momentum_invariance(f_in, g_in, F_ext=(15, -8))

    assert audit["is_momentum_strictly_preserved"] == True
    assert audit["delta_jx"] == 0
    assert audit["delta_jy"] == 0
    assert audit["mass_guard_conserved"] == True
