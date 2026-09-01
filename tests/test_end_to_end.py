"""
End-to-End Simulation Tests for Two-Phase D2Q9 Dam-Break.
"""
import numpy as np
import pytest
from quantum.timestep_quantum import run_quantum_dambreak


def test_classical_reference_execution():
    hist = run_quantum_dambreak(mode="classical", nx=4, ny=4, timesteps=3)
    assert len(hist) == 4
    for record in hist:
        assert record["total_mass"] > 0.0
        assert record["total_liquid_mass"] > 0.0


def test_hybrid_mode_execution():
    hist = run_quantum_dambreak(mode="hybrid", nx=4, ny=4, timesteps=3)
    assert len(hist) == 4
    for record in hist:
        assert record["total_mass"] > 0.0
        assert record["p_success_mean"] > 0.0


def test_quantum_mode_execution():
    hist = run_quantum_dambreak(mode="quantum", nx=4, ny=4, timesteps=3)
    assert len(hist) == 4
    for record in hist:
        assert record["total_mass"] > 0.0
        assert record["p_success_mean"] > 0.0


def test_quantum_vs_classical_agreement():
    c_hist = run_quantum_dambreak(mode="classical", nx=4, ny=4, timesteps=2)
    q_hist = run_quantum_dambreak(mode="quantum", nx=4, ny=4, timesteps=2)

    # Step 1 agreement
    diff_rho1 = np.max(np.abs(q_hist[1]["rho"] - c_hist[1]["rho"]))
    diff_phi1 = np.max(np.abs(q_hist[1]["phi"] - c_hist[1]["phi"]))
    assert diff_rho1 < 1e-3
    assert diff_phi1 < 1e-3
