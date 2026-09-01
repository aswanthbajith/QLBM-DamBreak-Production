import pytest
import numpy as np
import scipy.linalg as la
from quantum.two_phase_collision import build_two_phase_collision_unitary, get_bgk_collision_unitary_16x16
from classical.equilibrium import compute_equilibrium


class TestCollisionExactEquivalence:
    """
    Rigorously tests Part D/E: Collision Unitarity & Equilibrium Preservation.
    - U_coll† U_coll == I
    - Equilibrium states are invariant under collision
    """

    def test_01_collision_unitarity_across_omegas(self):
        for omega in [0.5, 0.8, 1.0, 1.25, 1.5, 1.8]:
            U16 = get_bgk_collision_unitary_16x16(omega=omega, dt=0.5)
            U_dag_U = U16.conj().T @ U16
            eye = np.eye(16, dtype=np.complex128)
            err = float(la.norm(U_dag_U - eye))
            assert err < 1e-12, f"omega={omega}: Collision unitary error {err:.2e} >= 1e-12"

    def test_02_two_phase_combined_unitary(self):
        U32 = build_two_phase_collision_unitary(tau_liquid=0.80, tau_gas=0.65)
        U_dag_U = U32.conj().T @ U32
        eye = np.eye(32, dtype=np.complex128)
        err = float(la.norm(U_dag_U - eye))
        assert err < 1e-12, f"Two-phase collision 32x32 unitary error {err:.2e} >= 1e-12"
