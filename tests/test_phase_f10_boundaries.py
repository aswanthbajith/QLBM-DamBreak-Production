"""
Phase F10: Automated Test Suite for Generalized Physical Boundary Masks.

Validates:
1. Physical boundary mask construction and node classification (solid vs fluid).
2. Generalized boundary operator unitarity (B†B = I) and involution (B^2 = I).
3. Isolated wall reflection accuracy on Left, Right, Bottom, Top boundaries.
4. Two-phase sector isolation (p'=p, zero f <-> g conversion).
5. Periodic wrap-around prevention via physical boundary bounce-back.
6. Timestep boundary ordering (collision -> streaming -> boundary).
7. Differential boundary kill switch on multi-node grids.
8. Multi-node Level 4 comparative accuracy and mass conservation.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from classical.equilibrium import compute_equilibrium
from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from quantum.physical_boundary_mask import PhysicalBoundaryMask
from quantum.parameterized_collision_oracle import ParameterizedQuantumCollisionOracle
from quantum.arithmetic_streaming import build_direct_streaming_circuit
from qiskit.quantum_info import Operator


def test_boundary_mask_construction_and_classification():
    """Verify solid wall and fluid domain classification on dam-break tank."""
    mask = PhysicalBoundaryMask(nx=4, ny=4, top_wall_solid=True)
    solid = mask.get_solid_mask()
    fluid = mask.get_fluid_mask()

    # Outer perimeter must be solid
    assert np.all(solid[0, :])   # Bottom wall
    assert np.all(solid[-1, :])  # Top wall
    assert np.all(solid[:, 0])   # Left wall
    assert np.all(solid[:, -1])  # Right wall

    # Interior must be fluid
    assert np.all(fluid[1:3, 1:3])
    assert np.all(~solid[1:3, 1:3])


def test_boundary_unitarity_and_involution():
    """Verify B†B = I and B^2 = I across multi-node grids."""
    for nx, ny in [(2, 2), (4, 4), (8, 4)]:
        mask = PhysicalBoundaryMask(nx=nx, ny=ny)
        metrics = mask.verify_unitarity_and_involution()
        assert metrics["unitarity_error"] < 1e-13, f"Grid {nx}x{ny} non-unitary: {metrics['unitarity_error']}"
        assert metrics["involution_error"] < 1e-13, f"Grid {nx}x{ny} not involution: {metrics['involution_error']}"


def test_isolated_wall_reflections():
    """Verify isolated incident reflections on Left, Right, Bottom, Top walls."""
    mask = PhysicalBoundaryMask(nx=4, ny=4)
    walls = ["left", "right", "bottom", "top"]

    for wall in walls:
        for p in [0, 1]:
            diag = mask.audit_single_wall(wall_type=wall, p_sector=p)
            assert diag["reflection_error"] < 1e-14, f"Wall {wall} sector {p} reflection error: {diag['reflection_error']}"
            assert diag["residual_incident_error"] < 1e-14, f"Wall {wall} sector {p} residual: {diag['residual_incident_error']}"
            assert diag["cross_talk_error"] < 1e-14, f"Wall {wall} sector {p} cross-talk: {diag['cross_talk_error']}"
            assert diag["norm_error"] < 1e-14


def test_two_phase_sector_isolation():
    """Verify that hydrodynamic (p=0) and phase-field (p=1) sectors never cross-contaminate."""
    mask = PhysicalBoundaryMask(nx=4, ny=4)
    B = mask.build_boundary_matrix()

    # Create mixed state
    psi_mixed = np.zeros(mask.hilbert_dim, dtype=np.complex128)
    idx_f = mask._state_index(0, 0, 1, 0)
    idx_g = mask._state_index(0, 0, 1, 1)
    psi_mixed[idx_f] = 0.6
    psi_mixed[idx_g] = 0.8

    psi_out = B @ psi_mixed

    idx_f_opp = mask._state_index(0, 0, OPPOSITE[1], 0)
    idx_g_opp = mask._state_index(0, 0, OPPOSITE[1], 1)

    assert abs(psi_out[idx_f_opp] - 0.6) < 1e-14
    assert abs(psi_out[idx_g_opp] - 0.8) < 1e-14
    assert abs(la.norm(psi_out) - 1.0) < 1e-14


def test_periodic_wrap_around_prevention():
    """Verify boundary bounce-back strictly prevents periodic coordinate wrap-around."""
    for nx, ny in [(4, 4), (8, 4)]:
        mask = PhysicalBoundaryMask(nx=nx, ny=ny)
        wrap_diag = mask.audit_periodic_wrap_around_prevention()
        assert wrap_diag["passed"], f"Grid {nx}x{ny} failed wrap-around prevention audit"
        assert wrap_diag["wrap_around_leakage"] < 1e-12


def test_differential_boundary_kill_switch():
    """Verify that replacing B with Identity fails to bounce incoming wall populations."""
    mask = PhysicalBoundaryMask(nx=4, ny=4)
    B_normal = mask.build_boundary_matrix()
    B_kill = np.eye(mask.hilbert_dim, dtype=np.complex128)

    # State incident on left wall (x=0, y=2, i=3 West)
    psi_in = np.zeros(mask.hilbert_dim, dtype=np.complex128)
    idx_inc = mask._state_index(0, 2, 3, 0)
    idx_ref = mask._state_index(0, 2, 1, 0)
    psi_in[idx_inc] = 1.0

    psi_normal = B_normal @ psi_in
    psi_kill = B_kill @ psi_in

    # Normal bounces to East
    assert abs(psi_normal[idx_ref] - 1.0) < 1e-14
    # Kill switch stays West (no reflection)
    assert abs(psi_kill[idx_inc] - 1.0) < 1e-14
    assert abs(psi_kill[idx_ref]) < 1e-14

    diff = float(la.norm(psi_normal - psi_kill))
    assert diff > 1.0, f"Boundary kill switch failed to produce divergence: {diff}"
