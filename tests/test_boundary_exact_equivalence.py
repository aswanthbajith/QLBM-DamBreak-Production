import pytest
import numpy as np
import scipy.linalg as la
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.two_phase_boundary import build_two_phase_boundary_unitary, build_two_phase_boundary_circuit
from classical.d2q9 import OPPOSITE


class TestBoundaryExactEquivalence:
    """
    Rigorously tests Part G: Boundary Condition Consistency.
    - Resolves bounce-back mechanism (half-way bounce-back on perimeter wall nodes)
    - Verifies U_bnd is an exact unitary involution (U_bnd^2 == I, U_bnd == U_bnd†)
    - Verifies exact matching of classical bounce-back reflections channel-by-channel
    - Verifies mass conservation across boundary operations
    """

    def test_01_involution_and_unitarity(self):
        for nx, ny in [(4, 4), (8, 4), (8, 8)]:
            layout = get_two_phase_register_layout(nx, ny)
            U = build_two_phase_boundary_unitary(layout)
            
            # 1. Check Unitarity: U† U == I
            U_dag_U = U.conj().T @ U
            eye = np.eye(U.shape[0], dtype=np.complex128)
            err_unit = float(la.norm(U_dag_U - eye))
            assert err_unit < 1e-12, f"Grid {nx}x{ny}: Boundary non-unitary error {err_unit:.2e} >= 1e-12"
            
            # 2. Check Involution: U^2 == I (bounce-back is self-inverse)
            U2 = U @ U
            err_inv = float(la.norm(U2 - eye))
            assert err_inv < 1e-12, f"Grid {nx}x{ny}: Boundary non-involution error {err_inv:.2e} >= 1e-12"

    def test_02_perimeter_wall_reflection_matching(self):
        nx, ny = 4, 4
        layout = get_two_phase_register_layout(nx, ny)
        U = build_two_phase_boundary_unitary(layout)
        
        n_qx = layout["n_qx"]
        n_qy = layout["n_qy"]
        n_qvel = layout["n_qvel"]
        
        # Check all nodes
        for p in [0, 1]:
            for i in range(9):
                for y in range(ny):
                    for x in range(nx):
                        idx_in = (p << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                        vec_in = np.zeros(U.shape[0], dtype=np.complex128)
                        vec_in[idx_in] = 1.0
                        
                        vec_out = U @ vec_in
                        out_idx = int(np.argmax(np.abs(vec_out)))
                        
                        is_wall = (x == 0 or x == nx - 1 or y == 0 or y == ny - 1)
                        i_expected = OPPOSITE[i] if is_wall else i
                        idx_expected = (p << (n_qx + n_qy + n_qvel)) | (i_expected << (n_qx + n_qy)) | (y << n_qx) | x
                        
                        assert out_idx == idx_expected, f"Boundary error at node ({x},{y}), channel {i}: got {out_idx}, expected {idx_expected}"

    def test_03_mass_conservation_on_boundary(self):
        nx, ny = 4, 4
        layout = get_two_phase_register_layout(nx, ny)
        U = build_two_phase_boundary_unitary(layout)
        
        # Generate random state
        psi = np.random.uniform(-1, 1, U.shape[0]) + 1j * np.random.uniform(-1, 1, U.shape[0])
        psi /= np.linalg.norm(psi)
        
        psi_bnd = U @ psi
        assert np.isclose(np.linalg.norm(psi_bnd), 1.0, atol=1e-12)
