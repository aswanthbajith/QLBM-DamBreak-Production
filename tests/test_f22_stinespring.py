"""
Phase F22: Test Suite for Stinespring Dilation and CPTP Channel Properties.
"""

import pytest
import numpy as np

from quantum.f22_stinespring import F22StinespringDilationProof


def test_stinespring_isometry_and_cptp():
    """Verify isometry, trace preservation, and Choi complete positivity."""
    dim = 4
    mapping = {0: 1, 1: 2, 2: 2, 3: 0}  # Non-injective map (0 and 1 relax to same state)
    proof = F22StinespringDilationProof(dim, mapping)

    # 1. Isometry test: V^\dagger V = I
    res_iso, is_iso = proof.verify_isometry()
    assert is_iso == True
    assert res_iso < 1e-12

    # 2. Trace preservation: \sum K^\dagger K = I
    res_tp, is_tp = proof.verify_trace_preservation()
    assert is_tp == True
    assert res_tp < 1e-12

    # 3. Choi complete positivity: \lambda_{\min} >= 0
    choi_audit = proof.audit_complete_positivity()
    assert choi_audit["is_completely_positive"] == True
    assert choi_audit["is_trace_preserving"] == True
    assert choi_audit["is_cptp"] == True
