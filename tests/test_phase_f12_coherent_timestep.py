"""
Phase F12: Test Suite for Autonomous Multi-Step Quantum Timestep Solver.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.coherent_timestep import PhaseF12AutonomousQLBM


def test_autonomous_multi_step_solver_execution():
    """Verify autonomous multi-step quantum solver without intermediate classical decoding."""
    solver = PhaseF12AutonomousQLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.001)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_quantum_timesteps == 0

    # Execute 5 consecutive quantum timesteps
    for _ in range(5):
        solver.step()

    assert solver.num_quantum_timesteps == 5
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0  # Zero intermediate classical extractions

    # Final decode
    final_fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
    assert "f" in final_fields and "g" in final_fields
    assert float(np.sum(final_fields["f"])) > 0.0


def test_autonomous_vs_level4_comparison():
    """Verify autonomous multi-step solver matches classical reference."""
    c_solver = Level4TwoPhaseLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.5, dam_height_ratio=0.5)
    q_solver = PhaseF12AutonomousQLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.5, dam_height_ratio=0.5)

    for _ in range(5):
        c_solver.step()
        q_solver.step()

    final_fields = q_solver.decode_final_fields()
    err_f = float(np.max(np.abs(final_fields["f"] - c_solver.f)))
    err_g = float(np.max(np.abs(final_fields["g"] - c_solver.g)))

    assert err_f < 1e-2, f"Autonomous solver f error: {err_f}"
    assert err_g < 1e-2, f"Autonomous solver g error: {err_g}"
