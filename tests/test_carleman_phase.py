import pytest
import numpy as np
from quantum.carleman_two_phase_step import quantum_carleman_two_phase_step


class TestCarlemanPhase:
    """
    Rigorously tests Level I: Phase-Volume Conservation and Boundedness.
    """

    def test_01_phase_field_bounds_and_liquid_conservation(self):
        history = quantum_carleman_two_phase_step(nx=4, ny=4, timesteps=5, order=2, use_block_encoding=True)
        liq0 = history[0]["total_liquid_mass"]
        for record in history:
            phi = record["phi"]
            assert np.all(phi >= -1e-10) and np.all(phi <= 1.0 + 1e-10), "Phase field exceeded [0, 1] bounds"
            drift = abs(record["total_liquid_mass"] - liq0) / liq0
            assert drift < 0.05, f"Liquid volume drift {drift*100:.2f}% >= 5%"
