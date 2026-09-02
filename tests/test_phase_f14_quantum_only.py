"""
Phase F14: Strict Quantum-Only Multi-Step Execution Test Suite.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.quantum_only_solver import StrictQuantumOnlyQLBM


def test_strict_quantum_only_execution():
    """Verify that strict quantum solver executes multi-step evolution with zero intermediate classical access."""
    solver = StrictQuantumOnlyQLBM(nx=4, ny=4)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0
    assert solver.num_quantum_timesteps == 0

    # Advance 16 timesteps via pure unitary matrix-vector evolution
    for _ in range(16):
        solver.step()

    assert solver.num_quantum_timesteps == 16
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    # Readout only at step T
    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
    assert "f" in fields and "g" in fields
    assert float(np.sum(fields["f"])) > 0.0


def test_strict_quantum_only_state_norm_evolution():
    """Verify quantum state norm remains strictly bounded during multi-step evolution."""
    solver = StrictQuantumOnlyQLBM(nx=2, ny=2)

    initial_norm = float(la.norm(solver.psi))
    assert abs(initial_norm - 1.0) < 1e-12

    for _ in range(8):
        solver.step()

    final_norm = float(la.norm(solver.psi))
    assert final_norm > 0.0 and final_norm <= 1.0000001
