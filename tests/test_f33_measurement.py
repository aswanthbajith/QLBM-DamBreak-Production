"""
Phase F33: Test Suite for Observable Extraction & Shot Convergence.
"""

import pytest
import numpy as np
from quantum.f33_measurement import F33MeasurementExtractor


def test_measurement_extraction_from_counts():
    """Verify field extraction from simulated bitstring counts."""
    counts = {"0010110000101100": 1000}  # Perfect state (liquid on left, gas on right)
    fields = F33MeasurementExtractor.extract_fields_from_counts(counts, nx=2, ny=2, bits_per_field=4)

    assert fields["total_shots"] == 1000
    assert fields["rho"].shape == (2, 2)
    assert fields["rho"][0, 0] > fields["rho"][0, 1]  # Liquid column higher than gas


def test_shot_convergence_scaling():
    """Verify standard error decreases as 1/sqrt(N)."""
    study = F33MeasurementExtractor.analyze_shot_convergence({}, shot_levels=[100, 10000])
    err_100 = study[0]["theoretical_stderr"]
    err_10000 = study[1]["theoretical_stderr"]

    assert abs(err_100 - 0.1) < 1e-5
    assert abs(err_10000 - 0.01) < 1e-5
    assert err_10000 < err_100
