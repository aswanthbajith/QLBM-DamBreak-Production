"""
Phase F25: Test Suite for Isolated Reversible Fixed-Point Arithmetic Primitives.
"""

import pytest
import numpy as np

from quantum.f25_reversible_primitives import F25ReversiblePrimitives


def test_reversible_add_sub_inverses():
    """Verify exact forward and inverse operations for add and sub."""
    prim = F25ReversiblePrimitives(frac_bits=8)

    a, b = 45, 120
    _, sum_ab = prim.reversible_add(a, b)
    assert sum_ab == 165
    _, b_rec = prim.reversible_add_inverse(a, sum_ab)
    assert b_rec == b

    _, diff_ba = prim.reversible_sub(a, b)
    assert diff_ba == 75
    _, b_orig = prim.reversible_sub_inverse(a, diff_ba)
    assert b_orig == b


def test_reversible_multiply_uncompute():
    """Verify forward multiplication and exact mirror uncomputation residual zero."""
    prim = F25ReversiblePrimitives(frac_bits=8)

    a = 256  # 1.0 in Q8.8
    b = 384  # 1.5 in Q8.8
    _, _, prod = prim.reversible_multiply(a, b)
    assert prod == 384  # 1.0 * 1.5 = 1.5

    _, _, residual = prim.reversible_multiply_uncompute(a, b, prod)
    assert residual == 0


def test_reversible_compare_select():
    """Verify reversible comparison and conditional selection with uncomputation."""
    prim = F25ReversiblePrimitives(frac_bits=8)

    a, b = 100, 200
    _, _, flag = prim.reversible_compare(a, b)
    assert flag == 1
    _, _, res_flag = prim.reversible_compare_uncompute(a, b, flag)
    assert res_flag == 0

    _, _, _, val = prim.reversible_select(flag, a, b)
    assert val == a
    _, _, _, res_val = prim.reversible_select_uncompute(flag, a, b, val)
    assert res_val == 0


def test_reversible_reciprocal_and_sqrt():
    """Verify fixed-point reciprocal and square root approximations."""
    prim = F25ReversiblePrimitives(frac_bits=8)

    # Reciprocal of 2.0 (512 in Q8.8) -> 0.5 (128 in Q8.8)
    x = 512
    _, recip = prim.reversible_reciprocal(x)
    assert recip == 128  # 1/2 = 0.5

    # Square root of 4.0 (1024 in Q8.8) -> 2.0 (512 in Q8.8)
    x_sq = 1024
    _, root = prim.reversible_sqrt(x_sq)
    assert root == 512  # sqrt(4.0) = 2.0
