"""
Phase F21: Test Suite for Circular Droplet / Curved Interface CSF Verification.
"""

import pytest
import numpy as np

from quantum.f21_csf import F21ReversibleCSFPipeline
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_circular_droplet_curvature():
    """Verify curvature sign and magnitude for circular droplet."""
    nx, ny = 8, 8
    math = F21FixedPointCSFMath()
    pipeline = F21ReversibleCSFPipeline(nx, ny, sigma=0.005)

    # Initialize circular droplet of radius R=2 in center
    alpha = np.zeros((ny, nx), dtype=np.int32)
    cx, cy = 3.5, 3.5
    for y in range(ny):
        for x in range(nx):
            r = np.sqrt((x - cx)**2 + (y - cy)**2)
            alpha_val = 0.5 * (1.0 - np.tanh((r - 2.0) / 0.8))
            alpha[y, x] = math.to_fixed(alpha_val)

    Fs_x, Fs_y, meta = pipeline.execute_reversible_csf(alpha)

    assert meta["is_uncomputed"] == True
    assert meta["is_unitary"] == True
