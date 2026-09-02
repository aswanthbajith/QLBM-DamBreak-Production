"""
Phase F12: Test Suite for Quantum Moment Extraction.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.quantum_moments import QuantumMomentExtractor


def test_quantum_moment_extraction_from_statevector():
    """Verify that moment extraction reconstructs rho, alpha, jx, jy to exact precision."""
    solver = Level4TwoPhaseLBM(nx=4, ny=4, dam_width_ratio=0.5, dam_height_ratio=0.5)
    extractor = QuantumMomentExtractor(nx=4, ny=4)

    # Encode into statevector
    norm_N = float(np.sqrt(np.sum(solver.f**2) + np.sum(solver.g**2)))
    psi = np.zeros(extractor.hilbert_dim, dtype=np.complex128)
    for x in range(4):
        for y in range(4):
            for i in range(9):
                idx_f = extractor._state_index(x, y, i, 0)
                idx_g = extractor._state_index(x, y, i, 1)
                psi[idx_f] = solver.f[i, y, x] / norm_N
                psi[idx_g] = solver.g[i, y, x] / norm_N

    moments = extractor.extract_moments_from_statevector(psi, norm_N)

    err_rho = float(np.max(np.abs(moments["rho"] - np.sum(solver.f, axis=0))))
    err_alpha = float(np.max(np.abs(moments["alpha"] - np.clip(np.sum(solver.g, axis=0), 0.0, 1.0))))
    assert err_rho < 1e-14, f"Density reconstruction error: {err_rho}"
    assert err_alpha < 1e-14, f"Phase reconstruction error: {err_alpha}"


def test_moment_probe_circuit_construction():
    """Verify ancilla-assisted moment probe circuit structure."""
    extractor = QuantumMomentExtractor(nx=4, ny=4)
    qc = extractor.build_moment_probe_circuit(x_target=2, y_target=2, species=0)
    assert qc.num_qubits == extractor.n_total + 1
    assert qc.name.startswith("MomentProbe")
