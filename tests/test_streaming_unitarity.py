"""
Unit tests for Quantum Streaming Operator and Circuit Module.
"""
import numpy as np
import scipy.linalg as la
import pytest
from classical.two_phase import initialize_two_phase_dambreak
from quantum.state_preparation import get_two_phase_register_layout
from quantum.streaming import (
    apply_quantum_streaming,
    build_two_phase_streaming_unitary,
    build_two_phase_streaming_circuit,
    build_two_phase_streaming_inverse_circuit
)


def test_streaming_operator_unitarity():
    layout = get_two_phase_register_layout(4, 4)
    S = build_two_phase_streaming_unitary(layout)
    dim = 512

    assert S.shape == (dim, dim)
    err_unitarity = la.norm(S.conj().T @ S - np.eye(dim, dtype=np.complex128))
    assert err_unitarity < 1e-12


def test_streaming_reversibility():
    layout = get_two_phase_register_layout(4, 4)
    S = build_two_phase_streaming_unitary(layout)
    dim = 512

    S_inv = S.conj().T
    err_reversibility = la.norm(S_inv @ S - np.eye(dim, dtype=np.complex128))
    assert err_reversibility < 1e-12


def test_streaming_array_consistency():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    f_stream, g_stream = apply_quantum_streaming(f, g)

    # Mass must be strictly preserved by permutation
    assert np.isclose(np.sum(f_stream), np.sum(f), atol=1e-12)
    assert np.isclose(np.sum(g_stream), np.sum(g), atol=1e-12)


def test_streaming_circuit_synthesis():
    layout = get_two_phase_register_layout(4, 4)
    qc = build_two_phase_streaming_circuit(layout)
    qc_inv = build_two_phase_streaming_inverse_circuit(layout)

    assert qc.num_qubits == 9
    assert qc_inv.num_qubits == 9
