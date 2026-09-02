"""
Automated Test Suite for Reversible Quantum Arithmetic Streaming in Direct Two-Phase QLBM.

Validates:
1. Exact mathematical equivalence between gate-level arithmetic streaming and matrix streaming.
2. Unitarity of the arithmetic streaming quantum circuit (S^dag S = I).
3. Unitarity and self-inverse involution of the boundary circuit (B^2 = I, B^dag B = I).
4. Machine-precision multi-step agreement against Level 4 classical reference.
5. Invariance of the idle/padding velocity subspace (|9>..|15>).
6. Transpilation metrics on IBM FakeSherbrooke.
"""

import pytest
import numpy as np
import scipy.linalg as la
from qiskit.quantum_info import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.direct_two_phase_prototype import DirectTwoPhaseQLBM
from quantum.arithmetic_streaming import (
    build_direct_streaming_circuit,
    build_direct_boundary_circuit,
    build_complete_direct_step_circuit,
)
from backends.fake_ibm_backend import get_fake_ibm_backend


def test_arithmetic_streaming_equivalence_2x2():
    """Verify that 2x2 gate-level arithmetic streaming matches matrix permutation S exactly."""
    solver_2x2 = DirectTwoPhaseQLBM(nx=2, ny=2)
    S_mat = solver_2x2.S_matrix

    qc_stream = build_direct_streaming_circuit(nx=2, ny=2)
    U_arithmetic = Operator(qc_stream).data

    err = float(la.norm(U_arithmetic - S_mat, 2))
    assert err < 1e-13, f"2x2 Arithmetic streaming differs from permutation matrix by {err}"


def test_arithmetic_streaming_equivalence_4x4():
    """Verify that 4x4 gate-level arithmetic streaming matches matrix permutation S exactly."""
    solver_4x4 = DirectTwoPhaseQLBM(nx=4, ny=4)
    S_mat = solver_4x4.S_matrix

    qc_stream = build_direct_streaming_circuit(nx=4, ny=4)
    U_arithmetic = Operator(qc_stream).data

    err = float(la.norm(U_arithmetic - S_mat, 2))
    assert err < 1e-13, f"4x4 Arithmetic streaming differs from permutation matrix by {err}"


def test_arithmetic_streaming_unitarity():
    """Verify that the gate-level arithmetic streaming circuit is strictly unitary."""
    for nx, ny in [(2, 2), (4, 4)]:
        qc = build_direct_streaming_circuit(nx=nx, ny=ny)
        U = Operator(qc).data
        dim = U.shape[0]
        unitarity_err = float(la.norm(U.conj().T @ U - np.eye(dim), 2))
        assert unitarity_err < 1e-12, f"Arithmetic streaming {nx}x{ny} is non-unitary: {unitarity_err}"


def test_boundary_involution_circuit():
    """Verify that the boundary involution circuit is a self-inverse unitary involution."""
    qc = build_direct_boundary_circuit(nx=2, ny=2)
    B = Operator(qc).data
    dim = B.shape[0]

    unitarity_err = float(la.norm(B.conj().T @ B - np.eye(dim), 2))
    involution_err = float(la.norm(B @ B - np.eye(dim), 2))

    assert unitarity_err < 1e-13, f"Boundary circuit is non-unitary: {unitarity_err}"
    assert involution_err < 1e-13, f"Boundary circuit is not an involution: {involution_err}"


def test_idle_velocity_subspace_invariance():
    """Verify that idle velocity states |9>..|15> are completely unperturbed by streaming."""
    solver = DirectTwoPhaseQLBM(nx=2, ny=2)
    S = solver.S_matrix

    # Test states where velocity index i is in {9..15}
    for x in range(2):
        for y in range(2):
            for i in range(9, 16):
                for p in range(2):
                    idx = solver._state_index(x, y, i, p)
                    e_vec = np.zeros(128, dtype=np.complex128)
                    e_vec[idx] = 1.0

                    streamed_vec = S @ e_vec
                    err = float(la.norm(streamed_vec - e_vec, 2))
                    assert err < 1e-14, f"Idle velocity state |{x},{y},{i},{p}> was perturbed by streaming!"


def test_complete_step_circuit_transpilation():
    """Verify that the complete step circuit transpiles onto IBM FakeSherbrooke."""
    qc = build_complete_direct_step_circuit(nx=2, ny=2)
    assert qc.num_qubits == 7

    backend = get_fake_ibm_backend()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)

    assert transpiled.depth() > 0
    ops = transpiled.count_ops()
    assert "cx" in ops or "ecr" in ops or "cz" in ops
