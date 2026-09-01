import pytest
import numpy as np
import scipy.linalg as la
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.two_phase_collision import build_two_phase_collision_unitary
from quantum.streaming import build_two_phase_streaming_unitary
from quantum.two_phase_boundary import build_two_phase_boundary_unitary


class TestOperatorUnitarity:
    """
    Rigorously tests Part L/S: Operator Unitarity across all components.
    """

    def test_01_all_quantum_operators_are_unitary(self):
        for nx, ny in [(4, 4), (8, 4)]:
            layout = get_two_phase_register_layout(nx, ny)
            dim = 1 << layout["total_qubits"]
            eye = np.eye(dim, dtype=np.complex128)
            
            # Streaming
            U_s = build_two_phase_streaming_unitary(layout)
            err_s = float(la.norm(U_s.conj().T @ U_s - eye))
            assert err_s < 1e-12, f"Streaming non-unitary: {err_s:.2e}"
            
            # Boundary
            U_b = build_two_phase_boundary_unitary(layout)
            err_b = float(la.norm(U_b.conj().T @ U_b - eye))
            assert err_b < 1e-12, f"Boundary non-unitary: {err_b:.2e}"
            
            # Collision (5q local block)
            U_c32 = build_two_phase_collision_unitary()
            err_c = float(la.norm(U_c32.conj().T @ U_c32 - np.eye(32, dtype=np.complex128)))
            assert err_c < 1e-12, f"Collision non-unitary: {err_c:.2e}"
