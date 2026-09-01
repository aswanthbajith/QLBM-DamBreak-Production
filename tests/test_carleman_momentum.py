import pytest
import numpy as np
from quantum.carleman_two_phase_step import quantum_carleman_two_phase_step


class TestCarlemanMomentum:
    """
    Rigorously tests Level H: Momentum & Velocity Field Properties of the Carleman QLBM Solver.
    """

    def test_01_velocity_boundedness_and_growth(self):
        history = quantum_carleman_two_phase_step(nx=4, ny=4, timesteps=5, order=2, use_block_encoding=True)
        for record in history:
            u = record["u"]
            u_mag = np.sqrt(u[0]**2 + u[1]**2)
            # Velocity magnitude must remain sub-critical (Mach < 1.0, u_mag < 0.80 in lattice units)
            assert np.all(u_mag < 0.80), f"Supersonic / unphysical velocity detected: {np.max(u_mag)}"
