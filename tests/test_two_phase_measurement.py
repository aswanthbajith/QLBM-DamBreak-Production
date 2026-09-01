import pytest
import numpy as np
from quantum.two_phase_step import reconstruct_two_phase_fields

class TestTwoPhaseMeasurement:
    def test_01_reconstruction_bounds(self):
        counts = {"000000000": 1000, "100000000": 1000}
        rho, u, phi = reconstruct_two_phase_fields(counts, nx=2, ny=2, total_mass=2.0)
        assert rho.shape == (2, 2)
        assert phi.shape == (2, 2)
        assert np.all(phi >= 0.0) and np.all(phi <= 1.0)
        assert np.isclose(np.sum(rho), 2.0, atol=1e-6)
