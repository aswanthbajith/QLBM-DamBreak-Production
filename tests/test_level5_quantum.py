"""
Unit and Integration Tests for Level-5 Quantum Two-Phase Solver.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level5_two_phase_quantum import Level5QuantumTwoPhaseSolver
from classical.level4_two_phase import Level4TwoPhaseLBM


class TestLevel5QuantumTwoPhase:
    """Test suite for Level-5 Quantum Two-Phase components."""

    def test_01_quantum_register_layout(self):
        """Verify quantum register sizes and dimensions."""
        solver = Level5QuantumTwoPhaseSolver(nx=4, ny=4)
        assert solver.total_sys_qubits == 9
        assert solver.dim_sys == 512
        assert solver.dim_total == 1024

    def test_02_state_encoding_decoding_roundtrip(self):
        """Verify exact lossless roundtrip encoding and decoding of f and g."""
        solver = Level5QuantumTwoPhaseSolver(nx=4, ny=4)
        classical = Level4TwoPhaseLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.0)

        f_orig = np.copy(classical.f)
        g_orig = np.copy(classical.g)

        psi, M_total = solver.encode_state(f_orig, g_orig)
        assert abs(la.norm(psi) - 1.0) < 1e-12

        f_rec, g_rec = solver.decode_state(psi, M_total)

        diff_f = la.norm(f_rec - f_orig)
        diff_g = la.norm(g_rec - g_orig)

        assert diff_f < 1e-12, f"Encoding roundtrip f error too high: {diff_f:.4e}"
        assert diff_g < 1e-12, f"Encoding roundtrip g error too high: {diff_g:.4e}"

    def test_03_streaming_unitarity(self):
        """Verify spatial streaming matrix S is strictly unitary."""
        solver = Level5QuantumTwoPhaseSolver(nx=4, ny=4)
        S = solver.S
        assert S.shape == (512, 512)
        diff = la.norm(S.conj().T @ S - np.eye(512), 2)
        assert diff < 1e-12, f"Streaming matrix not unitary: {diff:.4e}"

    def test_04_boundary_involution(self):
        """Verify boundary reflection operator B is an exact orthogonal involution."""
        solver = Level5QuantumTwoPhaseSolver(nx=4, ny=4)
        B = solver.B
        assert B.shape == (512, 512)
        diff_unitary = la.norm(B.conj().T @ B - np.eye(512), 2)
        diff_involution = la.norm(B @ B - np.eye(512), 2)
        assert diff_unitary < 1e-12, f"Boundary matrix not unitary: {diff_unitary:.4e}"
        assert diff_involution < 1e-12, f"Boundary matrix not involution: {diff_involution:.4e}"

    def test_05_end_to_end_step_execution(self):
        """Verify full quantum step execution returns valid moments and mass."""
        solver = Level5QuantumTwoPhaseSolver(nx=4, ny=4, g_acc=-0.0005)
        classical = Level4TwoPhaseLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.0)

        f_init = np.copy(classical.f)
        g_init = np.copy(classical.g)

        f_next, g_next, meta = solver.step(f_init, g_init)

        assert f_next.shape == (9, 4, 4)
        assert g_next.shape == (9, 4, 4)
        assert meta["p_success"] > 0.0
        assert meta["liquid_mass"] > 0.0
