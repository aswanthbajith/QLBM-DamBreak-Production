"""
Phase F27: Test Suite for Gate-Level Adjoint / Inverse Circuit Verification.
"""

import pytest
from quantum.f27_circuit_ir import ReversibleCircuitIR


def test_circuit_ir_exact_inversion():
    """Verify that C_inv * C is the exact identity operator on all basis states."""
    circ = ReversibleCircuitIR(num_qubits=3, name="ForwardCirc")
    circ.x(0)
    circ.cx(0, 1)
    circ.ccx(0, 1, 2)

    inv_circ = circ.inverse()

    for b0 in [0, 1]:
        for b1 in [0, 1]:
            for b2 in [0, 1]:
                init_state = [b0, b1, b2]
                fwd_state = circ.execute(init_state)
                restored_state = inv_circ.execute(fwd_state)
                assert restored_state == init_state
