"""
Phase F14: Test Suite for Unitarity, Involution, and Operator Properties.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.quantum_only_solver import StrictQuantumOnlyQLBM


def test_streaming_and_boundary_unitarity():
    """Verify S_arith and B_mask unitarity and involution."""
    solver = StrictQuantumOnlyQLBM(nx=2, ny=2)

    # 1. Streaming matrix unitarity
    S = solver.S_mat
    err_S = float(la.norm(S.conj().T @ S - np.eye(solver.hilbert_dim), 2))
    assert err_S < 1e-12, f"Streaming matrix non-unitary: {err_S}"

    # 2. Boundary mask involution and unitarity: B^2 = I, B^dagger B = I
    B = solver.B_mat
    err_B2 = float(la.norm(B @ B - np.eye(solver.hilbert_dim), 2))
    err_B_unit = float(la.norm(B.conj().T @ B - np.eye(solver.hilbert_dim), 2))
    assert err_B2 < 1e-12, f"Boundary mask not involution: {err_B2}"
    assert err_B_unit < 1e-12, f"Boundary mask non-unitary: {err_B_unit}"
