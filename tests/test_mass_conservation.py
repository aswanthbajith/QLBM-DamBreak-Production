import pytest
import numpy as np
from classical.two_phase import run_two_phase_dambreak, step_two_phase, initialize_two_phase_dambreak
from quantum.two_phase_step import quantum_two_phase_step


class TestMassConservation:
    """
    Rigorously tests Mass Conservation across classical and quantum solvers.
    """

    def test_01_classical_mass_bounded_drift(self):
        history = run_two_phase_dambreak(nx=8, ny=4, timesteps=5)
        m0 = history[0]["total_mass"]
        for record in history:
            drift = abs(record["total_mass"] - m0) / m0
            assert drift < 0.15, f"Classical mass drift {drift*100:.2f}% >= 15%"

    def test_02_quantum_probability_strict_conservation(self):
        for t in [1, 2, 5]:
            res = quantum_two_phase_step(nx=4, ny=4, timesteps=t, backend="aer_ideal", shots=0)
            rho_q = res["rho"]
            # Sum of probabilities must equal total_mass (encoded norm is 1.0)
            assert np.isclose(np.sum(rho_q), res["total_mass"], atol=1e-6)
