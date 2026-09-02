"""
Phase F25: Test Suite for Scaling Analysis and Bottleneck Hierarchy.
"""

import pytest
from quantum.f25_scaling_analysis import F25ScalingAnalysis


def test_precision_scaling_monotonicity():
    """Verify monotonic gate count growth with fractional bit-width."""
    table = F25ScalingAnalysis.get_precision_scaling_table()

    assert len(table) == 4
    for i in range(len(table) - 1):
        assert table[i]["toffolis_per_node"] < table[i + 1]["toffolis_per_node"]
        assert table[i]["qubits_per_node"] < table[i + 1]["qubits_per_node"]


def test_bottleneck_ranking_structure():
    """Verify top bottleneck rankings are identified."""
    ranks = F25ScalingAnalysis.rank_computational_bottlenecks()

    assert len(ranks) == 4
    assert ranks[0]["rank"] == 1
    assert "Polynomial Multiplications" in ranks[0]["component"]
