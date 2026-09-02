"""
Phase F21: Test Suite for End-to-End Reversible CSF Pipeline and Uncomputation.
"""

import pytest
import numpy as np

from quantum.f21_csf import F21ReversibleCSFPipeline
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_reversible_csf_pipeline_uncomputation():
    """Verify 100% uncomputation of intermediate stencil registers back to |0>."""
    nx, ny = 4, 4
    sigma = 0.001
    math = F21FixedPointCSFMath()
    pipeline = F21ReversibleCSFPipeline(nx, ny, sigma=sigma)

    alpha_reg = np.zeros((ny, nx), dtype=np.int32)
    alpha_reg[:2, :2] = math.to_fixed(1.0)  # Dam column in bottom-left

    Fs_x, Fs_y, meta = pipeline.execute_reversible_csf(alpha_reg)

    assert meta["is_uncomputed"] == True
    assert meta["garbage_residual"] == 0.0
    assert meta["is_unitary"] == True
    assert np.any(Fs_x != 0) or np.any(Fs_y != 0)
