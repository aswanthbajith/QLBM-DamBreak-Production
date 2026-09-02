"""
Phase F21: Test Suite for CSF CPTP Quantum Channel Properties.
"""

import pytest
from quantum.f21_channel import F21CSFChannelVerification


def test_csf_channel_cptp_properties():
    """Verify trace preservation and complete positivity of CSF channel."""
    dim = 4
    mapping = {0: 1, 1: 2, 2: 2, 3: 0}
    verifier = F21CSFChannelVerification(dim, mapping)

    res = verifier.verify_csf_channel_cptp()
    assert res["is_trace_preserving"] == True
    assert res["is_completely_positive"] == True
    assert res["is_cptp"] == True
    assert res["trace_preservation_residual"] < 1e-12
