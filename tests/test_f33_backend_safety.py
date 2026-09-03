"""
Phase F33: Test Suite for Real QPU Safety Gate Verification.
"""

import pytest
import os
from quantum.f33_backend import F33BackendManager


def test_real_qpu_safety_gate_disabled():
    """Verify real QPU execution is blocked by default when flags are unset."""
    backend, meta = F33BackendManager.get_real_qpu_backend()

    assert backend is None
    assert meta["is_active"] == False
    assert "BLOCKED" in meta["status"]
