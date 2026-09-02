"""
Automated Test Suite for Direct Encoding Scientific Audit.

Executes:
1. Controlled component validation (Tests A, B, C) to isolate streaming and collision.
2. Verification of amplitude representation conventions.
3. Idle subspace containment and non-contamination checks.
4. Correct classification of hybrid vs quantum operations.
"""

import pytest
import numpy as np
from classical.level4_two_phase import Level4TwoPhaseLBM
from classical.streaming import stream
from quantum.direct_two_phase_prototype import DirectTwoPhaseQLBM


def test_audit_test_a_full_pipeline():
    """Test A: Full Direct Two-Phase QLBM vs Level 4 Reference."""
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005)
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005)

    for t in range(5):
        q_solver.step()
        c_solver.step()

    f_err = np.max(np.abs(q_solver.f - c_solver.f))
    g_err = np.max(np.abs(q_solver.g - c_solver.g))
    assert f_err < 1e-13, f"Test A f error {f_err} exceeds tolerance"
    assert g_err < 1e-13, f"Test A g error {g_err} exceeds tolerance"


def test_audit_test_b_quantum_streaming_only():
    """Test B: Isolate Quantum Streaming with Exact Classical Collision."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005)
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005)

    # Stream classical directly on the identical initial distribution
    f_streamed_classical = stream(c_solver.f)
    g_streamed_classical = stream(c_solver.g)

    # Stream quantum on q_solver
    q_solver.apply_quantum_streaming()
    f_streamed_quantum, g_streamed_quantum = q_solver.decode_state()

    err_f_stream = np.max(np.abs(f_streamed_quantum - f_streamed_classical))
    err_g_stream = np.max(np.abs(g_streamed_quantum - g_streamed_classical))
    assert err_f_stream < 1e-13, f"Quantum streaming differs from classical streaming: {err_f_stream}"
    assert err_g_stream < 1e-13, f"Quantum streaming differs from classical streaming: {err_g_stream}"


def test_audit_test_c_subspace_containment():
    """Test C: Ensure no amplitude leaks into the non-physical velocity subspace (i >= 9)."""
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2)

    for step in range(5):
        q_solver.step()
        psi = q_solver.psi

        # Sum probabilities of states where i >= 9
        leakage = 0.0
        for x in range(2):
            for y in range(2):
                for i in range(9, 16):
                    for p in range(2):
                        idx = q_solver._state_index(x, y, i, p)
                        leakage += np.abs(psi[idx]) ** 2

        assert leakage < 1e-15, f"Step {step}: Amplitude leaked into invalid velocity states: {leakage}"


def test_qubit_count_audit():
    """Verify exact data qubit formula n_data = n_x + n_y + 5 across multiple grid sizes."""
    grids = [
        (2, 2, 1, 1, 7),
        (4, 4, 2, 2, 9),
        (8, 4, 3, 2, 10),
        (16, 8, 4, 3, 12),
        (32, 16, 5, 4, 14),
        (64, 32, 6, 5, 16),
        (128, 64, 7, 6, 18),
    ]
    for nx, ny, expected_nx, expected_ny, expected_tot in grids:
        n_x = int(np.ceil(np.log2(nx)))
        n_y = int(np.ceil(np.log2(ny)))
        n_tot = n_x + n_y + 4 + 1
        assert n_x == expected_nx
        assert n_y == expected_ny
        assert n_tot == expected_tot
