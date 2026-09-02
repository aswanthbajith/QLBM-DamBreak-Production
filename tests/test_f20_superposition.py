"""
Phase F20: Unit Test Suite for Superposition and Coherence Reduction.
"""

import pytest
import numpy as np

from quantum.f20_channel import F20QuantumChannel
from quantum.f20_superposition import F20SuperpositionAudit


def test_superposition_coherence_reduction():
    """Verify coherence behavior for collapsing and non-collapsing pairs."""
    dim = 4
    mapping = {0: 0, 1: 0, 2: 1, 3: 2}  # 0 and 1 collapse to 0
    channel = F20QuantumChannel(dim, mapping)
    audit = F20SuperpositionAudit(channel)

    # Test pair with identical output: 0 and 1 -> 0
    res_collapse = audit.test_superposition(x1=0, x2=1, theta=0.0)
    assert res_collapse["outputs_equal"] == True
    assert res_collapse["is_pure_output"] == True
    assert abs(res_collapse["trace_out"] - 1.0) < 1e-12

    # Test pair with different outputs: 0 and 2
    res_distinct = audit.test_superposition(x1=0, x2=2, theta=np.pi / 2)
    assert res_distinct["outputs_equal"] == False
    assert abs(res_distinct["trace_out"] - 1.0) < 1e-12
