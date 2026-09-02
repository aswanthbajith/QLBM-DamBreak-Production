"""
Phase F13: Test Suite for Coherent Quantum Moment Generation.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.coherent_moments import CoherentMomentGenerator


def test_coherent_moment_generator_fields():
    """Verify coherent moment generator matches Level-4 macroscopic fields."""
    c_solver = Level4TwoPhaseLBM(nx=4, ny=4, dam_width_ratio=0.5, dam_height_ratio=0.5)
    generator = CoherentMomentGenerator(nx=4, ny=4, precision_format="Q4.12")

    norm_N = float(np.sqrt(np.sum(c_solver.f**2) + np.sum(c_solver.g**2)))
    psi = np.zeros(generator.hilbert_dim, dtype=np.complex128)
    for x in range(4):
        for y in range(4):
            for i in range(9):
                idx_f = generator._state_index(x, y, i, 0)
                idx_g = generator._state_index(x, y, i, 1)
                psi[idx_f] = c_solver.f[i, y, x] / norm_N
                psi[idx_g] = c_solver.g[i, y, x] / norm_N

    fields, costs = generator.generate_coherent_moment_fields(psi, norm_N)

    err_rho = float(np.max(np.abs(fields["rho"] - np.sum(c_solver.f, axis=0))))
    err_alpha = float(np.max(np.abs(fields["alpha"] - np.clip(np.sum(c_solver.g, axis=0), 0.0, 1.0))))

    assert err_rho < 1e-3, f"Coherent density error: {err_rho}"
    assert err_alpha < 1e-3, f"Coherent phase error: {err_alpha}"
    assert costs["toffoli"] > 0
    assert costs["cx"] > 0


def test_moment_accumulator_circuit():
    """Verify moment accumulator quantum circuit."""
    generator = CoherentMomentGenerator(nx=4, ny=4)
    qc = generator.build_moment_accumulator_circuit()
    assert qc.num_qubits == 37
    assert qc.name == "ReversibleMomentAccumulator"
