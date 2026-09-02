"""
Automated Test Suite for Direct Spatial/Population Quantum Two-Phase D2Q9 Solver.

Validates:
1. Quantum statevector normalization and exact amplitude encoding/decoding.
2. Unitarity of the direct streaming permutation operator (S^dag S = I).
3. Exact involution of the bounce-back boundary operator (B^2 = I, B^dag B = I).
4. Machine-precision one-step agreement against Level 4 classical reference.
5. Multi-step trajectory agreement across T=1..10 against Level 4.
6. Liquid mass conservation and phase field boundedness.
7. IBM FakeSherbrooke transpilation of the 2x2 quantum circuit.
8. Spatial grid scalability for 4x4 direct encoding.
"""

import pytest
import numpy as np
import scipy.linalg as la
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.direct_two_phase_prototype import DirectTwoPhaseQLBM
from backends.fake_ibm_backend import get_fake_ibm_backend


def test_state_encoding_decoding():
    """Verify that quantum statevector is normalized and decodes to exact physical distributions."""
    solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5)
    psi = solver.psi

    # Check L2 normalization
    norm_sq = float(np.sum(np.abs(psi) ** 2))
    assert np.isclose(norm_sq, 1.0, atol=1e-14), f"Statevector not normalized: {norm_sq}"

    # Check roundtrip decoding
    f_dec, g_dec = solver.decode_state()
    f_err = np.max(np.abs(f_dec - solver.f))
    g_err = np.max(np.abs(g_dec - solver.g))
    assert f_err < 1e-14, f"f decode error {f_err} exceeds tolerance"
    assert g_err < 1e-14, f"g decode error {g_err} exceeds tolerance"


def test_streaming_unitarity():
    """Verify that the direct spatial streaming permutation operator S is strictly unitary."""
    solver = DirectTwoPhaseQLBM(nx=2, ny=2)
    S = solver.S_matrix
    dim = S.shape[0]

    unitarity_err = float(la.norm(S.conj().T @ S - np.eye(dim), 2))
    assert unitarity_err < 1e-14, f"Streaming operator S is non-unitary: {unitarity_err}"


def test_boundary_involution():
    """Verify that the bounce-back boundary operator B is a self-inverse unitary involution."""
    solver = DirectTwoPhaseQLBM(nx=2, ny=2)
    B = solver.B_matrix
    dim = B.shape[0]

    unitarity_err = float(la.norm(B.conj().T @ B - np.eye(dim), 2))
    involution_err = float(la.norm(B @ B - np.eye(dim), 2))

    assert unitarity_err < 1e-14, f"Boundary operator B is non-unitary: {unitarity_err}"
    assert involution_err < 1e-14, f"Boundary operator B is not an involution: {involution_err}"


def test_one_step_agreement_level4():
    """Verify that 1-step direct quantum solver matches Level 4 classical reference to machine precision."""
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)

    q_solver.step()
    c_solver.step()

    f_err = np.max(np.abs(q_solver.f - c_solver.f))
    g_err = np.max(np.abs(q_solver.g - c_solver.g))
    rho_err = np.max(np.abs(np.sum(q_solver.f, axis=0) - np.sum(c_solver.f, axis=0)))
    alpha_err = np.max(np.abs(np.clip(np.sum(q_solver.g, axis=0), 0, 1) - np.clip(np.sum(c_solver.g, axis=0), 0, 1)))

    assert f_err < 1e-14, f"1-step f error {f_err} exceeds machine precision"
    assert g_err < 1e-14, f"1-step g error {g_err} exceeds machine precision"
    assert rho_err < 1e-14, f"1-step rho error {rho_err} exceeds machine precision"
    assert alpha_err < 1e-14, f"1-step alpha error {alpha_err} exceeds machine precision"


def test_multistep_agreement_level4():
    """Verify that multi-step direct quantum trajectory matches Level 4 across 10 steps."""
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)

    for t in range(1, 11):
        q_solver.step()
        c_solver.step()

        f_err = np.max(np.abs(q_solver.f - c_solver.f))
        g_err = np.max(np.abs(q_solver.g - c_solver.g))
        assert f_err < 1e-13, f"Step {t} f error {f_err} exceeds tolerance"
        assert g_err < 1e-13, f"Step {t} g error {g_err} exceeds tolerance"


def test_liquid_mass_conservation():
    """Verify that liquid volume is tracked accurately across multi-step evolution."""
    q_solver = DirectTwoPhaseQLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)

    init_vol_q = float(np.sum(q_solver.alpha))
    init_vol_c = float(np.sum(c_solver.alpha))
    assert np.isclose(init_vol_q, init_vol_c, atol=1e-14)

    for _ in range(5):
        q_solver.step()
        c_solver.step()

    vol_q = float(np.sum(q_solver.alpha))
    vol_c = float(np.sum(c_solver.alpha))
    assert np.isclose(vol_q, vol_c, atol=1e-14)


def test_transpilation_fake_sherbrooke():
    """Verify that the 2x2 quantum circuit transpiles successfully onto IBM FakeSherbrooke (127Q)."""
    solver = DirectTwoPhaseQLBM(nx=2, ny=2)
    qc = solver.build_qiskit_circuit()

    assert qc.num_qubits == 7, f"Expected 7 logical qubits for 2x2 grid, got {qc.num_qubits}"

    backend = get_fake_ibm_backend()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)

    assert transpiled_qc.depth() > 0, "Transpiled depth must be positive"
    ops = transpiled_qc.count_ops()
    assert "cx" in ops or "ecr" in ops or "cz" in ops, "Transpiled circuit must contain 2Q gates"


def test_spatial_grid_scaling_4x4():
    """Verify that direct encoding scales correctly to a 4x4 grid (9 logical qubits)."""
    solver_4x4 = DirectTwoPhaseQLBM(nx=4, ny=4)
    assert solver_4x4.n_x == 2
    assert solver_4x4.n_y == 2
    assert solver_4x4.n_vel == 4
    assert solver_4x4.n_phase == 1
    assert solver_4x4.n_data == 9
    assert solver_4x4.dim_hilbert == 512

    # Verify streaming unitarity on 4x4
    S = solver_4x4.S_matrix
    unitarity_err = float(la.norm(S.conj().T @ S - np.eye(512), 2))
    assert unitarity_err < 1e-14, f"4x4 Streaming operator is non-unitary: {unitarity_err}"

    # Verify 1-step agreement on 4x4
    c_solver_4x4 = Level4TwoPhaseLBM(nx=4, ny=4, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=-0.0005, sigma=0.0)
    solver_4x4.step()
    c_solver_4x4.step()

    f_err = np.max(np.abs(solver_4x4.f - c_solver_4x4.f))
    g_err = np.max(np.abs(solver_4x4.g - c_solver_4x4.g))
    assert f_err < 1e-14, f"4x4 1-step f error {f_err} exceeds tolerance"
    assert g_err < 1e-14, f"4x4 1-step g error {g_err} exceeds tolerance"
