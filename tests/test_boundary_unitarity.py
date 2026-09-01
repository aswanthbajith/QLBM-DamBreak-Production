"""
Unit tests for Quantum Boundary Involution Operator and Circuit Module.
"""
import numpy as np
import scipy.linalg as la
import pytest
from classical.d2q9 import OPPOSITE, C_X, C_Y
from quantum.state_preparation import get_two_phase_register_layout
from quantum.boundary_quantum import (
    apply_quantum_boundary,
    build_two_phase_boundary_unitary,
    build_two_phase_boundary_circuit
)


def test_boundary_unitarity_and_involution():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    dim = 512

    assert B.shape == (dim, dim)
    # 1. Unitarity: B† B = I
    err_unitarity = la.norm(B.conj().T @ B - np.eye(dim, dtype=np.complex128))
    assert err_unitarity < 1e-12

    # 2. Involution: B² = I
    err_involution = la.norm(B @ B - np.eye(dim, dtype=np.complex128))
    assert err_involution < 1e-12

    # 3. Hermiticity: B† = B
    err_hermitian = la.norm(B.conj().T - B)
    assert err_hermitian < 1e-12


def test_left_wall_reflection():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    x = 0
    y = 2 # non-corner left wall
    # West direction i=3 (cx=-1, cy=0) hits left wall, must swap with East i=1 (cx=+1, cy=0)
    idx_w = (0 << (n_qx + n_qy + n_qvel)) | (3 << (n_qx + n_qy)) | (y << n_qx) | x
    idx_e = (0 << (n_qx + n_qy + n_qvel)) | (1 << (n_qx + n_qy)) | (y << n_qx) | x

    state_w = np.zeros(512, dtype=np.complex128)
    state_w[idx_w] = 1.0
    out = B @ state_w
    assert np.isclose(out[idx_e], 1.0, atol=1e-12)


def test_right_wall_reflection():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    x = 3
    y = 2 # non-corner right wall
    # East direction i=1 (cx=+1, cy=0) hits right wall, must swap with West i=3
    idx_e = (0 << (n_qx + n_qy + n_qvel)) | (1 << (n_qx + n_qy)) | (y << n_qx) | x
    idx_w = (0 << (n_qx + n_qy + n_qvel)) | (3 << (n_qx + n_qy)) | (y << n_qx) | x

    state_e = np.zeros(512, dtype=np.complex128)
    state_e[idx_e] = 1.0
    out = B @ state_e
    assert np.isclose(out[idx_w], 1.0, atol=1e-12)


def test_bottom_and_top_walls():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    # Bottom wall y=0: South i=4 (cy=-1) swaps with North i=2 (cy=+1)
    x = 2
    y = 0
    idx_s = (0 << (n_qx + n_qy + n_qvel)) | (4 << (n_qx + n_qy)) | (y << n_qx) | x
    idx_n = (0 << (n_qx + n_qy + n_qvel)) | (2 << (n_qx + n_qy)) | (y << n_qx) | x
    state_s = np.zeros(512, dtype=np.complex128)
    state_s[idx_s] = 1.0
    out = B @ state_s
    assert np.isclose(out[idx_n], 1.0, atol=1e-12)

    # Top wall y=3: North i=2 (cy=+1) swaps with South i=4
    y = 3
    idx_n_top = (0 << (n_qx + n_qy + n_qvel)) | (2 << (n_qx + n_qy)) | (y << n_qx) | x
    idx_s_top = (0 << (n_qx + n_qy + n_qvel)) | (4 << (n_qx + n_qy)) | (y << n_qx) | x
    state_n = np.zeros(512, dtype=np.complex128)
    state_n[idx_n_top] = 1.0
    out = B @ state_n
    assert np.isclose(out[idx_s_top], 1.0, atol=1e-12)


def test_corner_reflections():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    # Corner (x=0, y=0): South-West i=7 (cx=-1, cy=-1) hits both walls, swaps with North-East i=5 (cx=+1, cy=+1)
    x, y = 0, 0
    idx_sw = (0 << (n_qx + n_qy + n_qvel)) | (7 << (n_qx + n_qy)) | (y << n_qx) | x
    idx_ne = (0 << (n_qx + n_qy + n_qvel)) | (5 << (n_qx + n_qy)) | (y << n_qx) | x
    state_sw = np.zeros(512, dtype=np.complex128)
    state_sw[idx_sw] = 1.0
    out = B @ state_sw
    assert np.isclose(out[idx_ne], 1.0, atol=1e-12)


def test_tangential_and_interior_invariance():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    # Tangential: North i=2 at left wall (x=0, y=1) does not hit left wall (cx=0)
    x, y = 0, 1
    idx_tang = (0 << (n_qx + n_qy + n_qvel)) | (2 << (n_qx + n_qy)) | (y << n_qx) | x
    state_tang = np.zeros(512, dtype=np.complex128)
    state_tang[idx_tang] = 1.0
    out = B @ state_tang
    assert np.isclose(out[idx_tang], 1.0, atol=1e-12)

    # Interior: (x=1, y=1) for any direction i=1
    x, y = 1, 1
    idx_int = (0 << (n_qx + n_qy + n_qvel)) | (1 << (n_qx + n_qy)) | (y << n_qx) | x
    state_int = np.zeros(512, dtype=np.complex128)
    state_int[idx_int] = 1.0
    out = B @ state_int
    assert np.isclose(out[idx_int], 1.0, atol=1e-12)


def test_padding_states_invariance():
    layout = get_two_phase_register_layout(4, 4)
    B = build_two_phase_boundary_unitary(layout)
    n_qx, n_qy, n_qvel = layout["n_qx"], layout["n_qy"], layout["n_qvel"]

    # Padding state v=12 (>= 9)
    x, y = 0, 0
    idx_pad = (0 << (n_qx + n_qy + n_qvel)) | (12 << (n_qx + n_qy)) | (y << n_qx) | x
    state_pad = np.zeros(512, dtype=np.complex128)
    state_pad[idx_pad] = 1.0
    out = B @ state_pad
    assert np.isclose(out[idx_pad], 1.0, atol=1e-12)


def test_boundary_circuit_synthesis():
    layout = get_two_phase_register_layout(4, 4)
    qc = build_two_phase_boundary_circuit(layout)
    assert qc.num_qubits == 9
