import pytest
import numpy as np
import scipy.linalg as la
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.streaming import build_two_phase_streaming_unitary
from quantum.two_phase_boundary import build_two_phase_boundary_unitary


class TestCircuitInverse:
    """
    Rigorously tests Reversibility & Inverses of Permutation Operations.
    """

    def test_01_streaming_inverse_restores_state(self):
        nx, ny = 4, 4
        layout = get_two_phase_register_layout(nx, ny)
        U_s = build_two_phase_streaming_unitary(layout)
        
        # State vector
        dim = 1 << layout["total_qubits"]
        psi = np.random.uniform(-1, 1, dim) + 1j * np.random.uniform(-1, 1, dim)
        psi /= np.linalg.norm(psi)
        
        # Stream forward then backward (conjugate transpose)
        psi_streamed = U_s @ psi
        psi_restored = U_s.conj().T @ psi_streamed
        
        err = float(la.norm(psi_restored - psi))
        assert err < 1e-12, f"Streaming inverse error: {err:.2e}"

    def test_02_boundary_self_inverse(self):
        nx, ny = 4, 4
        layout = get_two_phase_register_layout(nx, ny)
        U_b = build_two_phase_boundary_unitary(layout)
        
        dim = 1 << layout["total_qubits"]
        psi = np.random.uniform(-1, 1, dim) + 1j * np.random.uniform(-1, 1, dim)
        psi /= np.linalg.norm(psi)
        
        # Bounce-back is an involution: U_b @ U_b == I
        psi_b = U_b @ psi
        psi_restored = U_b @ psi_b
        
        err = float(la.norm(psi_restored - psi))
        assert err < 1e-12, f"Boundary involution error: {err:.2e}"
