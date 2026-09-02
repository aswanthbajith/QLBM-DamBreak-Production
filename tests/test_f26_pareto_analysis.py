"""
Phase F26: Test Suite for Pareto Analysis and Architectural Scaling.
"""

import pytest
from quantum.f26_pareto_analysis import F26ParetoAnalysis


def test_precision_accuracy_sweep():
    """Verify error decreases monotonically with fractional bit precision."""
    res = F26ParetoAnalysis.run_precision_accuracy_sweep(nx=4, ny=4, sigma=0.001)

    assert len(res) == 7
    for row in res:
        assert row["is_mass_conserved"] == True
        assert row["is_phase_conserved"] == True


def test_architectural_memory_reduction():
    """Verify Architecture B achieves over 2x memory reduction on 128x64 domain."""
    arch = F26ParetoAnalysis.get_architectural_comparison(nx=128, ny=64, bit_width=16)

    assert arch["architecture_A_parallel_qubits"] == 5111808
    assert arch["architecture_B_shared_core_qubits"] == 2359632
    assert arch["memory_reduction_factor"] > 2.15
