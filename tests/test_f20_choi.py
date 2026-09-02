"""
Phase F20: Unit Test Suite for Choi Matrix and Complete Positivity.
"""

import pytest
import numpy as np

from quantum.f20_kraus import F20KrausRepresentation
from quantum.f20_choi import F20ChoiVerification


def test_choi_complete_positivity():
    """Verify J(E) >= 0, Tr(J(E)) = 1.0, Rank(J(E)) = D."""
    dim = 4
    mapping = {0: 0, 1: 0, 2: 1, 3: 2}
    kraus = F20KrausRepresentation(dim, mapping)
    choi = F20ChoiVerification(kraus)

    res = choi.audit_choi_properties()
    assert res["is_completely_positive"] == True
    assert res["is_cptp"] == True
    assert abs(res["trace"] - 1.0) < 1e-12
    assert res["min_eigenvalue"] >= -1e-12
    assert res["rank"] == dim
