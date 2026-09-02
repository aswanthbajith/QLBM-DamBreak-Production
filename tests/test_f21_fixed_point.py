"""
Phase F21: Test Suite for Fixed-Point Square Root and Arithmetic Bounds.
"""

import pytest
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_fixed_point_math_accuracy():
    """Verify integer square root and division precision."""
    math = F21FixedPointCSFMath(frac_bits=12)

    # Test sqrt(4.0) = 2.0
    val_fixed = math.to_fixed(4.0)
    sqrt_fixed = math.fixed_sqrt(val_fixed)
    assert abs(math.to_float(sqrt_fixed) - 2.0) < 1e-3

    # Test sqrt(0.25) = 0.5
    val_fixed2 = math.to_fixed(0.25)
    sqrt_fixed2 = math.fixed_sqrt(val_fixed2)
    assert abs(math.to_float(sqrt_fixed2) - 0.5) < 1e-3
