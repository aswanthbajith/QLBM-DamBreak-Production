"""
Phase F20: Unit Test Suite for Kraus Operator Derivation and Trace Preservation.
"""

import pytest
import numpy as np

from quantum.f20_kraus import F20KrausRepresentation


def test_kraus_trace_preservation():
    """Verify sum_mu K_mu^dag K_mu = I."""
    dim = 8
    mapping = {i: (i // 2) for i in range(dim)}  # 2-to-1 non-injective map
    kraus = F20KrausRepresentation(dim, mapping)

    residual, is_tp = kraus.verify_trace_preservation()
    assert is_tp == True
    assert residual < 1e-12
