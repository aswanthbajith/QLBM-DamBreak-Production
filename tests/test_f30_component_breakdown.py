"""
Phase F30: Test Suite for Component-Level Reversible Gate Breakdown.
"""

import pytest
from quantum.f30_scaling_engine import F30ScalingEngine


def test_component_breakdown_metrics():
    """Verify component-level Toffoli and T-count formulas."""
    breakdown = F30ScalingEngine.get_component_gate_breakdown(bit_width=16)

    assert len(breakdown) == 7
    total_toffoli = sum(c["toffoli"] for c in breakdown)
    assert total_toffoli == 21168

    max_workspace = max(c["workspace"] for c in breakdown)
    assert max_workspace == 48  # Strictly 48 qubits peak workspace
