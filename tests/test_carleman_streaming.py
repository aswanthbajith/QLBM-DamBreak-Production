import pytest
import numpy as np
import scipy.linalg as la
from classical.streaming import stream
from classical.reference_solver import stream_two_phase


class TestCarlemanStreaming:
    """
    Rigorously tests Step 9: Streaming Exact Permutation Properties.
    """

    def test_01_two_phase_streaming_preserves_total_mass(self):
        np.random.seed(42)
        f = np.random.uniform(0.1, 1.0, (9, 4, 4))
        g = np.random.uniform(0.0, 1.0, (9, 4, 4))
        
        m_f_0 = np.sum(f)
        m_g_0 = np.sum(g)
        
        f_s, g_s = stream_two_phase(f, g)
        
        assert np.isclose(np.sum(f_s), m_f_0)
        assert np.isclose(np.sum(g_s), m_g_0)
