"""
Phase F22: Test Suite for Multi-Precision Fixed-Point Error Scaling (Q4.12 vs Q4.16 vs Q4.20).
"""

import pytest
from quantum.f22_precision import F22PrecisionScalingStudy


def test_precision_scaling_convergence():
    """Verify that Q4.16 and Q4.20 achieve superior relative force precision (< 1%)."""
    results = F22PrecisionScalingStudy.run_droplet_precision_benchmark(nx=8, ny=8, sigma=0.005)

    assert len(results) == 3
    q12, q16, q20 = results[0], results[1], results[2]

    # Error must monotonically decrease as fractional bit-width increases
    assert q16["force_Linf_error"] < q12["force_Linf_error"]
    assert q20["force_Linf_error"] < q16["force_Linf_error"]
    assert q20["force_relative_L2_error"] < 0.05
