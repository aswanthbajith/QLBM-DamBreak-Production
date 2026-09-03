"""
Phase F37: Test Suite for Macroscopic Observables Reconstruction.
"""

import pytest
from quantum.f37_observables_reconstruction import F37ObservablesReconstructor


def test_observables_reconstruction():
    """Verify density and phase extraction from bitstrings."""
    counts = {"0010110000101100": 2048}
    fields = F37ObservablesReconstructor.reconstruct_from_counts(counts, nx=2, ny=2, bits_per_node=4)

    assert fields["total_shots"] == 2048
    assert fields["rho"].shape == (2, 2)
    assert fields["rho"][0, 0] > fields["rho"][0, 1]  # Liquid column higher than gas
    assert fields["total_mass"] > 0
