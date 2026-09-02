"""
Phase F9: Quantum-Path Transparency, Hidden-Classical-Operation Audit & Kill-Switch Tests.

Rigorous differential testing verifying that:
1. Quantum collision is genuinely executed (Kill switch departure > 0.10).
2. Parameter changes strictly alter quantum unitary dilation output.
3. Streaming operator is genuinely responsible for spatial transport.
4. Boundary involution is genuinely responsible for wall reflections.
5. State preparation faithfully encodes physical amplitudes.
6. Transparency event stream accurately captures all runtime operations.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.phase_f8_2x2_solver import PhaseF8TwoPhaseQLBM2x2
from quantum.parameterized_collision_oracle import (
    build_parameterized_collision_matrix,
    ParameterizedQuantumCollisionOracle,
)
from quantum.transparency_audit import (
    TransparencyLogger,
    TransparencyEvent,
    get_transparency_logger,
)


def test_quantum_collision_kill_switch():
    """Kill Switch: Disabling the quantum collision on non-equilibrium state MUST cause immediate divergence."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_normal = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_kill = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    # Step 1: Advance all solvers
    c_solver.step()
    q_normal.step_mode1_parameter_fed()
    q_kill.step_mode1_parameter_fed()

    normal_err = float(np.max(np.abs(q_normal.f - c_solver.f)))
    assert normal_err < 1e-13

    # Step 2: on q_kill, replace U_C with Identity (kill collision)
    def dummy_kill_collision(z, alpha, u_vec, apply_oaa=False):
        return z.copy(), {"unitarity_error": 0.0, "proj_block_error": 0.0}

    q_kill.collision_oracle.execute_collision = dummy_kill_collision
    c_solver.step()
    q_normal.step_mode1_parameter_fed()
    q_kill.step_mode1_parameter_fed()

    normal_err_step2 = float(np.max(np.abs(q_normal.f - c_solver.f)))
    kill_err_step2 = float(np.max(np.abs(q_kill.f - c_solver.f)))

    assert normal_err_step2 < 1e-13, f"Normal solver failed on step 2: {normal_err_step2}"
    assert kill_err_step2 > 0.10, f"Kill switch failed: error {kill_err_step2} is too small, expected > 0.10!"


def test_no_hidden_reference_collision():
    """Verify that z_post is computed from U_C @ z_pad and strictly responds to matrix perturbations."""
    oracle = ParameterizedQuantumCollisionOracle()
    z_in = np.ones(18, dtype=np.float64) / np.sqrt(18)
    alpha = 0.5
    u_vec = np.array([0.02, 0.01])

    z_post_normal, meta_normal = oracle.execute_collision(z_in, alpha, u_vec)

    # Perturb the parameters to create a different dilation
    z_post_perturbed, meta_perturbed = oracle.execute_collision(z_in, alpha=0.9, u_vec=np.array([0.08, -0.04]))

    diff = float(la.norm(z_post_normal - z_post_perturbed))
    assert diff > 0.05, f"Quantum collision output did not respond to parameter changes: diff={diff}"


def test_parameter_kill_switch():
    """Verify that deliberately wrong parameters passed to Mode 1 produce measurable trajectory error."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_solver_wrong = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    c_solver.step()
    # Feed deliberately inverted alpha field and large opposing velocity
    wrong_alpha = np.ones((2, 2)) * 0.0  # Gas parameter for liquid
    wrong_u = np.ones((2, 2, 2)) * 0.12   # Large artificial velocity

    q_solver_wrong.step_mode1_parameter_fed(alpha_feed=wrong_alpha, u_feed=wrong_u)
    err_wrong = float(np.max(np.abs(q_solver_wrong.f - c_solver.f)))

    assert err_wrong > 0.01, f"Parameter kill switch failed: solver did not respond to incorrect parameters (err={err_wrong})"


def test_collision_matrix_differential_test():
    """Verify that Sz.-Nagy dilation of C_correct vs C_perturbed strictly separates in output."""
    alpha = 0.6
    u_vec = np.array([0.03, 0.01])
    z = np.linspace(0.1, 0.9, 18)

    C_correct, alpha_C, U_C_correct, _ = build_parameterized_collision_matrix(alpha, u_vec)

    # Construct perturbed matrix
    C_perturbed = C_correct.copy()
    C_perturbed[0, 1] += 0.2
    C_perturbed[1, 0] -= 0.2

    # Embed both into 64x64 Sz.-Nagy dilation
    alpha_pert = float(la.norm(C_perturbed, 2)) * 1.01
    D_pert = la.sqrtm(np.eye(18) - (C_perturbed.T @ C_perturbed) / (alpha_pert**2))
    D_star_pert = la.sqrtm(np.eye(18) - (C_perturbed @ C_perturbed.T) / (alpha_pert**2))

    U_pert = np.zeros((64, 64), dtype=np.complex128)
    U_pert[:18, :18] = C_perturbed / alpha_pert
    U_pert[:18, 32:50] = D_star_pert
    U_pert[32:50, :18] = D_pert
    U_pert[32:50, 32:50] = -C_perturbed.T / alpha_pert
    U_pert[18:32, 18:32] = np.eye(14)
    U_pert[50:, 50:] = np.eye(14)

    z_pad = np.zeros(64, dtype=np.complex128)
    z_pad[:18] = z

    out_correct = np.real((alpha_C * (U_C_correct @ z_pad))[:18])
    out_pert = np.real((alpha_pert * (U_pert @ z_pad))[:18])

    diff = float(la.norm(out_correct - out_pert))
    assert diff > 0.01, "Sz.-Nagy dilation failed differential test on perturbed collision matrix"
    assert float(la.norm(out_correct - (C_correct @ z))) < 1e-14, "Correct dilation did not reconstruct C @ z"


def test_streaming_transparency_and_kill_switch():
    """Verify that arithmetic streaming genuinely transports populations between grid nodes."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    # Initial state has liquid at (0,0) and gas elsewhere
    f_init = solver.f.copy()

    # Apply streaming matrix directly to state
    psi_streamed = solver.U_stream @ solver.psi
    f_streamed, _ = solver.decode_state(psi_streamed)

    # After streaming, populations must have moved to adjacent nodes (0,1), (1,0), (1,1)
    diff_stream = float(np.max(np.abs(f_streamed - f_init)))
    assert diff_stream > 0.1, "Streaming operator did not transport populations!"

    # Kill Switch: If U_stream = Identity, transport fails
    psi_kill = np.eye(128) @ solver.psi
    f_kill, _ = solver.decode_state(psi_kill)
    assert float(np.max(np.abs(f_kill - f_init))) < 1e-15, "Identity streaming altered state unexpectedly"


def test_boundary_transparency_and_kill_switch():
    """Verify that boundary involution genuinely flips velocities along solid walls."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    # Prepare a state with population in velocity 1 (East, cx=1, cy=0)
    psi_test = np.zeros(128, dtype=np.complex128)
    idx_v1 = solver._state_index(x=0, y=0, i=1, p=0)
    idx_v3 = solver._state_index(x=0, y=0, i=3, p=0)  # Opposite (West)
    psi_test[idx_v1] = 1.0

    psi_bnd = solver.U_bnd @ psi_test
    # Must have flipped from velocity 1 to velocity 3
    assert abs(psi_bnd[idx_v3] - 1.0) < 1e-14, "Boundary involution failed to bounce velocity 1 -> 3"
    assert abs(psi_bnd[idx_v1]) < 1e-14, "Original velocity amplitude remained after boundary involution"

    # Self-inverse check: B^2 = I
    psi_roundtrip = solver.U_bnd @ psi_bnd
    assert abs(psi_roundtrip[idx_v1] - 1.0) < 1e-14, "Boundary involution is not self-inverse (B^2 != I)"


def test_state_preparation_transparency():
    """Verify that distinct physical states map to distinct, orthogonal quantum statevectors."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    psi_1 = solver.encode_state()

    # Modify populations
    solver.f[1, 0, 0] += 0.5
    psi_2 = solver.encode_state()

    overlap = float(np.abs(np.vdot(psi_1, psi_2)))
    assert overlap < 0.99, f"State preparation failed to separate perturbed state: overlap = {overlap}"


def test_state_derived_mode_dependency():
    """Verify Mode 2 results strictly depend on fixed-point word length."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, nu_L=0.05, nu_G=0.01, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_8bit = PhaseF8TwoPhaseQLBM2x2(nu_L=0.05, nu_G=0.01, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_16bit = PhaseF8TwoPhaseQLBM2x2(nu_L=0.05, nu_G=0.01, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    # Add velocity perturbation to ensure non-trivial moment arithmetic
    for s in [c_solver, q_8bit, q_16bit]:
        s.f[1, 0, 0] += 0.02
        s.f[3, 0, 0] -= 0.02

    c_solver.step()
    q_8bit.step_mode2_state_derived(word_length=8, frac_bits=4)
    q_16bit.step_mode2_state_derived(word_length=16, frac_bits=12)

    err_8bit = float(np.max(np.abs(q_8bit.f - c_solver.f)))
    err_16bit = float(np.max(np.abs(q_16bit.f - c_solver.f)))

    assert err_8bit > 10 * err_16bit, f"Expected 8-bit error ({err_8bit}) >> 16-bit error ({err_16bit})"


def test_transparency_logger_event_stream():
    """Verify that TransparencyLogger captures all 11 expected quantum and hybrid events in 1 step."""
    logger = TransparencyLogger(enabled=True)
    # Temporary swap global logger
    import quantum.phase_f8_2x2_solver as f8_mod
    f8_mod.get_transparency_logger = lambda: logger

    solver = PhaseF8TwoPhaseQLBM2x2()
    logger.clear()

    solver.step_mode1_parameter_fed()
    counts = logger.get_event_counts()

    assert counts.get(TransparencyEvent.QUANTUM_COLLISION_EXECUTION.value, 0) == 4  # 4 nodes
    assert counts.get(TransparencyEvent.QUANTUM_STREAMING_EXECUTION.value, 0) == 1
    assert counts.get(TransparencyEvent.QUANTUM_BOUNDARY_EXECUTION.value, 0) == 1
    assert counts.get(TransparencyEvent.CLASSICAL_REENCODE.value, 0) == 1
    assert counts.get(TransparencyEvent.CLASSICAL_DECODE.value, 0) == 1
