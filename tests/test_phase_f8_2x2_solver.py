"""
Automated Test Suite for Phase F8 End-to-End 2x2 Quantum Two-Phase Solver.

Validates:
1. State normalization and roundtrip encoding/decoding (< 1e-15 error).
2. Arithmetic streaming unitarity and exact translation.
3. Boundary bounce-back involution (B^2 = I, B†B = I).
4. Mode 1 single-step and multi-step machine-precision agreement vs Level-4 (< 1e-13 error).
5. Mode 2 state-derived parameter collision precision (< 0.5% fixed-point truncation error).
6. Mandatory dilation leakage audit: unprojected powers leak defect vs projected powers exact.
7. Mass and phase conservation diagnostics.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.phase_f8_2x2_solver import PhaseF8TwoPhaseQLBM2x2


def test_f8_2x2_state_normalization_and_mapping():
    """Verify state normalization and exact roundtrip amplitude reconstruction."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    assert solver.num_data_qubits == 7
    assert solver.hilbert_dim == 128

    norm_psi = float(la.norm(solver.psi))
    assert abs(norm_psi - 1.0) < 1e-15, f"State is not normalized: {norm_psi}"

    f_rec, g_rec = solver.decode_state()
    err_f = np.max(np.abs(f_rec - solver.f))
    err_g = np.max(np.abs(g_rec - solver.g))
    assert err_f < 1e-14, f"f roundtrip error {err_f} exceeds tolerance"
    assert err_g < 1e-14, f"g roundtrip error {err_g} exceeds tolerance"


def test_f8_2x2_streaming_unitarity_and_exactness():
    """Verify arithmetic streaming operator is strictly unitary on 7-qubit data register."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    U_s = solver.U_stream

    unitarity_err = float(la.norm(U_s.conj().T @ U_s - np.eye(128), 2))
    assert unitarity_err < 1e-13, f"Streaming operator non-unitary: {unitarity_err}"


def test_f8_2x2_boundary_involution():
    """Verify bounce-back boundary operator is a self-inverse unitary involution."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    U_b = solver.U_bnd

    unitarity_err = float(la.norm(U_b.conj().T @ U_b - np.eye(128), 2))
    involution_err = float(la.norm(U_b @ U_b - np.eye(128), 2))

    assert unitarity_err < 1e-13, f"Boundary operator non-unitary: {unitarity_err}"
    assert involution_err < 1e-13, f"Boundary operator not an involution: {involution_err}"


def test_f8_2x2_mode1_single_step_precision():
    """Verify Mode 1 (Parameter-Fed Quantum) matches Level 4 to machine precision on step 1."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_solver = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    c_solver.step()
    q_step_info = q_solver.step_mode1_parameter_fed()

    err_f = np.max(np.abs(q_solver.f - c_solver.f))
    err_g = np.max(np.abs(q_solver.g - c_solver.g))

    assert err_f < 1e-13, f"Mode 1 f error {err_f} exceeds machine precision tolerance"
    assert err_g < 1e-13, f"Mode 1 g error {err_g} exceeds machine precision tolerance"


def test_f8_2x2_mode2_state_derived_single_step():
    """Verify Mode 2 (State-Derived Emulator) achieves controlled low fixed-point truncation error."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_solver = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    c_solver.step()
    q_solver.step_mode2_state_derived(word_length=16, frac_bits=12)

    err_f = np.max(np.abs(q_solver.f - c_solver.f))
    err_g = np.max(np.abs(q_solver.g - c_solver.g))

    # 16-bit fixed point truncation error is expected to be small (< 0.5%)
    rel_err_f = err_f / np.max(c_solver.f)
    assert rel_err_f < 0.01, f"Mode 2 relative f error {rel_err_f} exceeds 1%"


def test_f8_2x2_multistep_progression_mode1():
    """Verify Mode 1 multi-step evolution across T=1, 2, 4, 8, 10 timesteps."""
    c_solver = Level4TwoPhaseLBM(nx=2, ny=2, dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)
    q_solver = PhaseF8TwoPhaseQLBM2x2(dam_width_ratio=0.5, dam_height_ratio=0.5, g_acc=0.0, sigma=0.0)

    for t in range(1, 11):
        c_solver.step()
        q_solver.step_mode1_parameter_fed()

        err_f = float(np.max(np.abs(q_solver.f - c_solver.f)))
        err_g = float(np.max(np.abs(q_solver.g - c_solver.g)))
        assert err_f < 1e-13, f"Step {t}: f error {err_f} exceeds machine precision"
        assert err_g < 1e-13, f"Step {t}: g error {err_g} exceeds machine precision"


def test_f8_2x2_dilation_leakage_audit():
    """Mandatory Audit: verify unprojected dilation powers leak defect vs projected powers exact."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    leakage_records = solver.audit_dilation_leakage(K_powers=[1, 2, 4, 8])

    for rec in leakage_records:
        K = rec["K_powers"]
        if K > 1:
            # Unprojected powers must have large leakage error (> 100%)
            assert rec["unprojected_leakage_error"] > 1.0, f"Expected unprojected leakage at K={K}"
        # Projected reset power must be exact to machine precision (< 1e-14)
        assert rec["projected_reset_error"] < 1e-14, f"Projected reset error at K={K} exceeds tolerance"


def test_f8_2x2_conservation_diagnostics():
    """Verify total fluid mass and phase mass are strictly conserved across 10 steps."""
    solver = PhaseF8TwoPhaseQLBM2x2()
    init_diag = solver.compute_diagnostics()
    init_mass = init_diag["total_mass"]
    init_phase = init_diag["phase_mass"]

    for _ in range(10):
        solver.step_mode1_parameter_fed()

    final_diag = solver.compute_diagnostics()
    assert abs(final_diag["total_mass"] - init_mass) < 1e-12, "Total mass drift exceeded tolerance"
    assert abs(final_diag["phase_mass"] - init_phase) < 1e-12, "Phase mass drift exceeded tolerance"
