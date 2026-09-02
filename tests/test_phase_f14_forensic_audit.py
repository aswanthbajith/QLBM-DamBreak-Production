"""
Phase F14: Forensic Audit & Anti-Hybrid Interlock Test Suite.
"""

import pytest
import numpy as np

from quantum.quantum_only_solver import StrictQuantumOnlyQLBM


def test_no_intermediate_extractions_during_evolution():
    """Verify that during multi-step quantum evolution, no classical extractions occur."""
    solver = StrictQuantumOnlyQLBM(nx=2, ny=2)

    for step_i in range(5):
        solver.step()
        assert solver.num_classical_extractions == 0
        assert solver.num_re_encodings == 0

    assert solver.num_quantum_timesteps == 5
    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
