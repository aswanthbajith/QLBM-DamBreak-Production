"""
Phase F30: Test Suite for Precision Scaling and Pareto Frontier (Q4.8 to Q4.20).
"""

import pytest
from quantum.f30_scaling_engine import F30ScalingEngine


def test_precision_pareto_front():
    """Verify Pareto knee at Q4.16 with exact error bounds."""
    pareto = F30ScalingEngine.calculate_precision_pareto_front()

    assert len(pareto) == 7
    q4_16 = [p for p in pareto if p["format"] == "Q4.16"][0]
    assert q4_16["is_pareto_knee"] == True
    assert q4_16["csf_force_error"] < 0.02
    assert q4_16["hydro_density_error"] < 5.0e-5
