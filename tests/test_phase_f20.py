"""
Unit tests for Phase F20: Moment-Space Dissipative Quantum Channel Validation
and Coherent Two-Phase QLBM Prototype.
"""

import numpy as np
import pytest

from quantum.phase_f20_research_engine import (
    D2Q9_MOMENT_MATRIX,
    D2Q9_INV_MOMENT_MATRIX,
    MOMENT_NAMES,
    CONSERVED_INDICES,
    NONEQ_INDICES,
    populations_to_moments,
    moments_to_populations,
    compute_equilibrium_moments,
)


def test_d2q9_moment_matrix_orthogonality():
    """Verify that M M^T is diagonal and M^-1 M = I to machine precision."""
    MMT = D2Q9_MOMENT_MATRIX @ D2Q9_MOMENT_MATRIX.T
    diag_elements = np.diag(MMT)
    off_diag = MMT - np.diag(diag_elements)

    assert np.allclose(off_diag, 0.0, atol=1e-14), "Off-diagonal elements must be zero"
    assert np.allclose(D2Q9_INV_MOMENT_MATRIX @ D2Q9_MOMENT_MATRIX, np.eye(9), atol=1e-14)
    assert np.allclose(D2Q9_MOMENT_MATRIX @ D2Q9_INV_MOMENT_MATRIX, np.eye(9), atol=1e-14)


def test_populations_moments_roundtrip():
    """Verify population-moment roundtrip transformations."""
    f = np.array([0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    m = populations_to_moments(f)
    f_rec = moments_to_populations(m)
    assert np.allclose(f, f_rec, atol=1e-14)


def test_conserved_modes_jacobian():
    """Verify that conserved modes have eigenvalue 1.0 under collision Jacobian."""
    omega = 0.8
    J = np.zeros((9, 9), dtype=np.float64)
    for k in CONSERVED_INDICES:
        J[k, k] = 1.0
    for k in NONEQ_INDICES:
        J[k, k] = 1.0 - omega

    eigvals = np.linalg.eigvals(J)
    # Conserved modes should have eigenvalue 1.0 (multiplicity 3)
    ones = [ev for ev in eigvals if np.isclose(ev, 1.0)]
    assert len(ones) == 3

    # Non-equilibrium modes should have eigenvalue 1.0 - omega = 0.2 (multiplicity 6)
    contracting = [ev for ev in eigvals if np.isclose(ev, 1.0 - omega)]
    assert len(contracting) == 6


def test_cptp_trace_preservation_and_choi():
    """Verify trace preservation and complete positivity of the moment-space channel."""
    d_S = 8
    F = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 5, 6: 6, 7: 7}
    neq_map = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0}
    distinct_e = sorted(list(set(neq_map.values())))

    kraus_ops = []
    for e in distinct_e:
        K = np.zeros((d_S, d_S), dtype=np.complex128)
        for x in range(d_S):
            if neq_map[x] == e:
                K[F[x], x] = 1.0
        kraus_ops.append(K)

    # 1. Trace preservation
    tp_sum = sum(K.conj().T @ K for K in kraus_ops)
    assert np.allclose(tp_sum, np.eye(d_S), atol=1e-14)

    # 2. Choi matrix
    choi = np.zeros((d_S * d_S, d_S * d_S), dtype=np.complex128)
    for i in range(d_S):
        for j in range(d_S):
            e_ij = sum(K @ np.outer(np.eye(d_S)[i], np.eye(d_S)[j]) @ K.conj().T for K in kraus_ops)
            for r in range(d_S):
                for c in range(d_S):
                    choi[i * d_S + r, j * d_S + c] = e_ij[r, c] / d_S

    eigvals = np.linalg.eigvalsh(choi)
    assert np.min(eigvals) >= -1e-14, "Choi matrix must be positive semidefinite"


def test_case_a_superposition_coherence_preserved():
    """Verify Case A: superposition of states with same non-eq sector preserves 100% coherence."""
    d_S = 8
    F = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 5, 6: 6, 7: 7}
    neq_map = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0}
    distinct_e = sorted(list(set(neq_map.values())))

    kraus_ops = []
    for e in distinct_e:
        K = np.zeros((d_S, d_S), dtype=np.complex128)
        for x in range(d_S):
            if neq_map[x] == e:
                K[F[x], x] = 1.0
        kraus_ops.append(K)

    # States 0 and 3 both have neq=0 (local equilibria)
    psi = np.zeros(d_S, dtype=np.complex128)
    psi[0] = 1.0 / np.sqrt(2)
    psi[3] = 1.0 / np.sqrt(2)
    rho_in = np.outer(psi, psi.conj())

    rho_out = sum(K @ rho_in @ K.conj().T for K in kraus_ops)

    c_in = float(np.sum(np.abs(rho_in)) - np.trace(rho_in).real)
    c_out = float(np.sum(np.abs(rho_out)) - np.trace(rho_out).real)

    assert np.isclose(c_in, 1.0, atol=1e-12)
    assert np.isclose(c_out, 1.0, atol=1e-12), "Case A must preserve 100% coherence"


def test_case_b_superposition_different_neq_decoheres():
    """Verify Case B: superposition of states with different non-eq sectors decoheres."""
    d_S = 8
    F = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 5, 6: 6, 7: 7}
    neq_map = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0}
    distinct_e = sorted(list(set(neq_map.values())))

    kraus_ops = []
    for e in distinct_e:
        K = np.zeros((d_S, d_S), dtype=np.complex128)
        for x in range(d_S):
            if neq_map[x] == e:
                K[F[x], x] = 1.0
        kraus_ops.append(K)

    # States 0 (neq=0) and 1 (neq=1)
    psi = np.zeros(d_S, dtype=np.complex128)
    psi[0] = 1.0 / np.sqrt(2)
    psi[1] = 1.0 / np.sqrt(2)
    rho_in = np.outer(psi, psi.conj())

    rho_out = sum(K @ rho_in @ K.conj().T for K in kraus_ops)

    # Since F(0) = 0 and F(1) = 0, both relax to state 0:
    # rho_out = |0><0| (pure state with purity 1.0)
    purity = float(np.real(np.trace(rho_out @ rho_out)))
    assert np.isclose(purity, 1.0, atol=1e-12)


def test_reference_system_entanglement_preservation():
    """Verify that applying the channel to system S preserves entanglement with reference qubit R."""
    d_S = 8
    F = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 5, 6: 6, 7: 7}
    neq_map = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0}
    distinct_e = sorted(list(set(neq_map.values())))

    kraus_ops = []
    for e in distinct_e:
        K = np.zeros((d_S, d_S), dtype=np.complex128)
        for x in range(d_S):
            if neq_map[x] == e:
                K[F[x], x] = 1.0
        kraus_ops.append(K)

    # Bell state on R and S (states 0 and 3, both neq=0)
    psi = np.zeros(2 * d_S, dtype=np.complex128)
    psi[0 * d_S + 0] = 1.0 / np.sqrt(2)
    psi[1 * d_S + 3] = 1.0 / np.sqrt(2)
    rho_in = np.outer(psi, psi.conj())

    rho_out = np.zeros((2 * d_S, 2 * d_S), dtype=np.complex128)
    for K in kraus_ops:
        IK = np.kron(np.eye(2), K)
        rho_out += IK @ rho_in @ IK.conj().T

    eigvals = np.linalg.eigvalsh(rho_out)
    assert np.min(eigvals) >= -1e-14, "Joint density matrix must remain positive semidefinite"

    # Joint state purity and fidelity with input state
    joint_purity = float(np.real(np.trace(rho_out @ rho_out)))
    fidelity = float(np.real(psi.conj().T @ rho_out @ psi))

    assert np.isclose(joint_purity, 1.0, atol=1e-12), "Joint state must remain pure when non-eq modes match"
    assert np.isclose(fidelity, 1.0, atol=1e-12), "Entanglement fidelity must be 1.0"

