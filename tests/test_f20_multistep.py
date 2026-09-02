"""
Phase F20: Unit Test Suite for Multi-Step Channel Composition E^K vs F^K.
"""

import pytest
import numpy as np

from quantum.f20_channel import F20QuantumChannel
from quantum.f20_multistep import F20MultiStepChannelAudit


def test_multistep_channel_equivalence():
    """Verify E^K(|x><x|) == |F^K(x)><F^K(x)| for K = 1, 2, 4, 8, 16."""
    dim = 8
    mapping = {0: 1, 1: 2, 2: 3, 3: 3, 4: 0, 5: 1, 6: 2, 7: 3}
    channel = F20QuantumChannel(dim, mapping)
    multi_audit = F20MultiStepChannelAudit(channel)

    for k in [1, 2, 4, 8, 16]:
        res = multi_audit.verify_multistep_equivalence(x0=4, k_steps=k)
        assert res["is_exact_multistep"] == True
        assert res["diff_frobenius"] < 1e-12
