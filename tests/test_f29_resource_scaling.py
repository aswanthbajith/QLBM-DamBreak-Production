"""
Phase F29: Test Suite for Logical Qubit Allocation Across Scalable Grid Sizes.
"""

import pytest


def test_qubit_scaling_formulas():
    """Verify total logical qubit allocation for 4x4, 8x8, 16x16 grids."""
    bit_width = 16
    work_qubits = 3 * bit_width  # 48

    # 4x4 (16 nodes)
    q_4x4 = (16 * 18 * bit_width) + (16 * 18 * bit_width) + work_qubits
    assert q_4x4 == 9264

    # 8x8 (64 nodes)
    q_8x8 = (64 * 18 * bit_width) + (64 * 18 * bit_width) + work_qubits
    assert q_8x8 == 36912

    # 16x16 (256 nodes)
    q_16x16 = (256 * 18 * bit_width) + (256 * 18 * bit_width) + work_qubits
    assert q_16x16 == 147504
