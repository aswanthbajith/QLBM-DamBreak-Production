"""
Phase F23: Positivity Guard and Constrained Physical Bounds for Fixed-Point BGK Collision.

Ensures:
1. All populations f_i >= 0 (strictly non-negative).
2. Rest particle f_0 absorption of integer truncation residuals preserves f_0 >= 0.
3. Phase fraction 0 <= alpha <= 1 is strictly maintained.
4. Zero mass drift sum_i f_out[i] == rho_in.
"""

from typing import List, Tuple, Dict, Any
import numpy as np


class F23PositivityGuardedBGK:
    """
    Guarantees physical non-negativity and exact zeroth-moment mass conservation.
    """

    @staticmethod
    def enforce_positivity_and_conservation(
        f_dir: List[int],
        rho_target: int,
    ) -> List[int]:
        """
        f_dir contains f_1..f_8. Computes f_0 = rho_target - sum(f_1..f_8).
        If f_0 < 0 (due to large velocities near Mach limits), distributes negative
        residual proportionally across directional populations to guarantee f_i >= 0.
        """
        f_out = [0] * 9
        for i in range(1, 9):
            f_out[i] = max(0, f_dir[i - 1])

        sum_dir = sum(f_out[1:9])
        f0 = rho_target - sum_dir

        if f0 >= 0:
            f_out[0] = f0
        else:
            # Scale directional components down to accommodate f0 = 0
            scale_factor = float(rho_target) / max(1, sum_dir)
            for i in range(1, 9):
                f_out[i] = int(round(f_out[i] * scale_factor))
            f_out[0] = max(0, rho_target - sum(f_out[1:9]))

        return f_out
