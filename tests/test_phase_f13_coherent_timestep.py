"""
Phase F13: Test Suite for Fully Coherent Autonomous Timestep Evolution.
"""

import pytest
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.coherent_timestep import PhaseF13AutonomousQLBM


def test_autonomous_evolution_operation_counts():
    """Verify operational counters for autonomous evolution: 1 preparation, 0 intermediate extractions/re-encodings."""
    solver = PhaseF13AutonomousQLBM(nx=4, ny=4)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0
    assert solver.num_quantum_timesteps == 0

    # Advance 8 quantum timesteps
    for _ in range(8):
        solver.step()

    assert solver.num_quantum_timesteps == 8
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    # Readout at termination
    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1


def test_coherent_vs_level4_accuracy():
    """Verify multi-step accuracy against Level-4 classical reference."""
    c_solver = Level4TwoPhaseLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.5, dam_height_ratio=0.5)
    q_solver = PhaseF13AutonomousQLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.5, dam_height_ratio=0.5)

    for _ in range(5):
        c_solver.step()
        q_solver.step()

    fields = q_solver.decode_final_fields()
    err_f = float(np.max(np.abs(fields["f"] - c_solver.f)))
    err_g = float(np.max(np.abs(fields["g"] - c_solver.g)))

    assert err_f < 1e-2, f"Coherent f error exceeded tolerance: {err_f}"
    assert err_g < 1e-2, f"Coherent g error exceeded tolerance: {err_g}"
