"""
Phase F20: Unit Test Suite for Quantum Channel Definition and Interpretation Equivalence.
"""

import pytest
import numpy as np

from quantum.f20_channel import F20QuantumChannel


def test_channel_stinespring_and_dephasing_equivalence():
    """Verify exact equivalence between Stinespring Kraus channel and Interpretation 2."""
    dim = 4
    mapping = {0: 1, 1: 1, 2: 3, 3: 0}  # Non-injective map: 0 and 1 collapse to 1
    channel = F20QuantumChannel(dim, mapping)

    # Random density matrix
    A = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    rho = A @ A.conj().T
    rho /= np.trace(rho)

    diff, is_exact = channel.check_interpretation_equivalence(rho)
    assert is_exact == True
    assert diff < 1e-12
