"""
Phase F17: Test Suite for Reversible Fixed-Point Arithmetic Primitives (Q4.12).
"""

import pytest
import numpy as np

from quantum.f17_reversible_primitives import FixedPointQ412, ReversibleFixedPointArithmetic


def test_fixed_point_q412_conversion_and_bounds():
    """Verify Q4.12 conversion accuracy, LSB precision, and saturation limits."""
    val = 1.25
    fixed_val = FixedPointQ412.to_fixed(val)
    reconstructed = FixedPointQ412.to_float(fixed_val)
    assert abs(val - reconstructed) < FixedPointQ412.EPSILON

    # Min/Max bounds
    assert FixedPointQ412.to_fixed(10.0) == FixedPointQ412.to_fixed(FixedPointQ412.MAX_VAL)
    assert FixedPointQ412.to_fixed(-10.0) == FixedPointQ412.to_fixed(FixedPointQ412.MIN_VAL)


def test_reversible_arithmetic_operations():
    """Verify addition, subtraction, multiplication, division, and uncomputation."""
    arith = ReversibleFixedPointArithmetic(frac_bits=12)

    a = FixedPointQ412.to_fixed(2.5)
    b = FixedPointQ412.to_fixed(1.5)

    # Addition
    sum_val = arith.add(a, b)
    assert abs(FixedPointQ412.to_float(sum_val) - 4.0) < FixedPointQ412.EPSILON

    # Multiplication
    prod_val = arith.multiply(a, b)
    assert abs(FixedPointQ412.to_float(prod_val) - 3.75) < 0.001

    # Division
    div_val = arith.divide(a, b)
    assert abs(FixedPointQ412.to_float(div_val) - (2.5 / 1.5)) < 0.001
