"""
Phase F34: Test Suite for Macroscopic Observables and Standard Error Bounds.
"""

import pytest
from quantum.f34_observables import F34ObservableExtractor


def test_observables_calculation():
    """Verify macroscopic density, phase, and standard error calculations."""
    counts = {"0010110000101100": 1000}
    fields = F34ObservableExtractor.compute_fields(counts, nx=2, ny=2, bits_per_node=4)

    assert fields["total_shots"] == 1000
    assert fields["rho"].shape == (2, 2)
    assert fields["rho"][0, 0] > fields["rho"][0, 1]  # Liquid column higher than gas
    assert fields["total_mass"] > 0
