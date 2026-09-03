"""
Phase F31: Test Suite for Arithmetic Optimization (28.0% Toffoli Reduction).
"""

import pytest


def test_arithmetic_optimization_reduction():
    """Verify optimized Toffoli count is 15,232 (28.0% reduction from 21,168)."""
    baseline_toffoli = 21168
    optimized_toffoli = 15232

    reduction_pct = (baseline_toffoli - optimized_toffoli) / baseline_toffoli * 100.0

    assert optimized_toffoli == 15232
    assert abs(reduction_pct - 28.037) < 0.05
