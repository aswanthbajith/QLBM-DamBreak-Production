"""
Phase F22: Test Suite for Physical Quantum State Representation and Encodings.
"""

import pytest
import numpy as np

from quantum.f22_quantum_state import F22PhysicalStateEncoding


def test_state_encoding_roundtrip():
    """Verify exact fixed-point basis state encoding and decoding."""
    encoding = F22PhysicalStateEncoding(frac_bits=12)

    f_orig = [0.4444, 0.1111, 0.1111, 0.1111, 0.1111, 0.0277, 0.0277, 0.0277, 0.0277]
    g_orig = [0.4444, 0.1111, 0.1111, 0.1111, 0.1111, 0.0277, 0.0277, 0.0277, 0.0277]

    f_reg, g_reg = encoding.encode_populations_to_basis_state(f_orig, g_orig)
    f_dec, g_dec = encoding.decode_basis_state_to_populations(f_reg, g_reg)

    max_err_f = max(abs(a - b) for a, b in zip(f_orig, f_dec))
    max_err_g = max(abs(a - b) for a, b in zip(g_orig, g_dec))

    assert max_err_f <= 1.0 / 4096
    assert max_err_g <= 1.0 / 4096


def test_statistical_density_matrix_properties():
    """Verify purity and von Neumann entropy of statistical mixtures."""
    encoding = F22PhysicalStateEncoding()

    states = [([1000] * 9, [500] * 9), ([2000] * 9, [1000] * 9)]
    probs = [0.6, 0.4]

    rho_dict = encoding.construct_statistical_density_matrix(states, probs)
    assert rho_dict["type"] == "COMPUTATIONAL_BASIS_STATISTICAL"
    assert abs(rho_dict["purity"] - (0.6**2 + 0.4**2)) < 1e-12
    assert rho_dict["von_neumann_entropy"] > 0.0
