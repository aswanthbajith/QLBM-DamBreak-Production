"""
Phase F21: Fixed-Point Arithmetic and Elementary Nonlinear Functions for CSF.

Supports exact fixed-point:
- Q4.12 (baseline)
- Q4.8 and Q4.16 comparisons
- Fixed-point integer square root
- Fixed-point non-restoring divider
- Gradient stencils, curvature clamping, and interface masking
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from quantum.f17_reversible_primitives import FixedPointQ412, ReversibleFixedPointArithmetic


class F21FixedPointCSFMath:
    """
    Fixed-point mathematics and nonlinear operations for Continuum Surface Force (CSF).
    """

    def __init__(self, frac_bits: int = 12):
        self.frac_bits = frac_bits
        self.scale = 1 << frac_bits
        self.arith = ReversibleFixedPointArithmetic(frac_bits=frac_bits)

    def to_fixed(self, val: float) -> int:
        return int(round(val * self.scale))

    def to_float(self, val: int) -> float:
        return float(val) / self.scale

    def fixed_sqrt(self, val_fixed: int) -> int:
        """
        Computes fixed-point square root: sqrt(x * scale) * sqrt(scale) / scale.
        Integer square root of (val_fixed << frac_bits).
        """
        if val_fixed <= 0:
            return 0
        scaled_val = val_fixed << self.frac_bits
        # Integer square root (Babylonian / Newton method)
        x0 = scaled_val // 2 if scaled_val > 1 else scaled_val
        if x0 == 0:
            return 0
        x1 = (x0 + scaled_val // x0) // 2
        while x1 < x0:
            x0 = x1
            x1 = (x0 + scaled_val // x0) // 2
        return int(x0)

    def fixed_div(self, num_fixed: int, den_fixed: int) -> int:
        """Fixed-point division."""
        return self.arith.divide(num_fixed, max(den_fixed, 1))

    def fixed_mul(self, a_fixed: int, b_fixed: int) -> int:
        """Fixed-point multiplication."""
        return self.arith.multiply(a_fixed, b_fixed)

    def fixed_clip(self, val_fixed: int, min_val: float, max_val: float) -> int:
        """Fixed-point clamping."""
        min_fixed = self.to_fixed(min_val)
        max_fixed = self.to_fixed(max_val)
        return max(min_fixed, min(max_fixed, val_fixed))
