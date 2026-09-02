"""
Phase F27: Test Suite for Gate-Level Reversible Circuit IR Execution.
"""

import pytest
from quantum.f27_circuit_ir import ReversibleCircuitIR
from quantum.f27_gate_primitives import F27GatePrimitives


def test_circuit_ir_gates_execution():
    """Verify X, CX, CCX, and SWAP execution on basis state bitstrings."""
    circ = ReversibleCircuitIR(num_qubits=4, name="TestCircuit")
    circ.x(0)
    circ.cx(0, 1)
    circ.ccx(0, 1, 2)
    circ.swap(2, 3)

    initial_state = [0, 0, 0, 0]
    out_state = circ.execute(initial_state)

    # Step 1: X(0) -> [1, 0, 0, 0]
    # Step 2: CX(0, 1) -> [1, 1, 0, 0]
    # Step 3: CCX(0, 1, 2) -> [1, 1, 1, 0]
    # Step 4: SWAP(2, 3) -> [1, 1, 0, 1]
    assert out_state == [1, 1, 0, 1]


def test_moment_accumulator_circuit():
    """Verify bit-level moment accumulator circuit."""
    circ = F27GatePrimitives.build_moment_accumulator(num_pops=4, bit_width=4)
    assert circ.num_qubits == (4 + 1) * 4
    metrics = circ.get_resource_metrics()
    assert metrics["cx_count"] == 16
