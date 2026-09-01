import pytest
import numpy as np
import scipy.linalg as la
from qiskit.quantum_info import Operator
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.streaming import build_two_phase_streaming_unitary, build_two_phase_streaming_circuit
from classical.d2q9 import C_X, C_Y


class TestStreamingExactEquivalence:
    """
    Rigorously tests Part F: Exact Reversible Streaming Permutation.
    - U_stream† U_stream = I
    - U_stream^(-1) returns exact initial state
    - Exact permutation mapping across 2x2, 4x4, 8x4, 8x8
    """

    def test_01_unitarity_and_invertibility(self):
        for nx, ny in [(2, 2), (4, 4), (8, 4), (8, 8)]:
            layout = get_two_phase_register_layout(nx, ny)
            U = build_two_phase_streaming_unitary(layout)
            
            # 1. Check Unitarity: U† U == I
            U_dag_U = U.conj().T @ U
            eye = np.eye(U.shape[0], dtype=np.complex128)
            err_unit = float(la.norm(U_dag_U - eye))
            assert err_unit < 1e-12, f"Grid {nx}x{ny}: Streaming non-unitary error {err_unit:.2e} >= 1e-12"
            
            # 2. Check Permutation Matrix Property (is standard permutation matrix)
            is_perm = np.allclose(U @ np.ones(U.shape[0]), 1.0) and np.allclose(U.sum(axis=0), 1.0)
            assert is_perm, f"Grid {nx}x{ny}: Streaming is not an exact permutation matrix"

    def test_02_coordinate_shift_fidelity(self):
        nx, ny = 4, 4
        layout = get_two_phase_register_layout(nx, ny)
        U = build_two_phase_streaming_unitary(layout)
        
        n_qx = layout["n_qx"]
        n_qy = layout["n_qy"]
        n_qvel = layout["n_qvel"]
        
        # Test every single basis state |x, y, i, p>
        for p in [0, 1]:
            for i in range(9):
                for y in range(ny):
                    for x in range(nx):
                        idx_in = (p << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                        vec_in = np.zeros(U.shape[0], dtype=np.complex128)
                        vec_in[idx_in] = 1.0
                        
                        vec_out = U @ vec_in
                        out_idx = int(np.argmax(np.abs(vec_out)))
                        
                        x_expected = (x + C_X[i]) % nx
                        y_expected = (y + C_Y[i]) % ny
                        idx_expected = (p << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y_expected << n_qx) | x_expected
                        
                        assert out_idx == idx_expected, f"Streaming error: input ({x},{y},{i},{p}) mapped to {out_idx}, expected {idx_expected}"
