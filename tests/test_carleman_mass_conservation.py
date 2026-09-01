import pytest
import numpy as np
from quantum.carleman_two_phase_step import quantum_carleman_two_phase_step


class TestCarlemanMassConservation:
    """
    Rigorously tests Level G: Mass Conservation of the Carleman QLBM Solver.
    """

    def test_01_total_mass_drift_bounded(self):
        history = quantum_carleman_two_phase_step(nx=4, ny=4, timesteps=5, order=2, use_block_encoding=True)
        m0 = history[0]["total_mass"]
        for record in history:
            drift = abs(record["total_mass"] - m0) / m0
            assert drift < 0.10, f"Mass drift {drift*100:.2f}% >= 10%"
