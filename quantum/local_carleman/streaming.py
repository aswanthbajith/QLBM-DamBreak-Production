"""
Local Spatial Streaming Permutation Circuit.
"""
from PHASE11_STREAMING_ORACLE import build_d2q9_streaming_circuit

def build_local_streaming_circuit(nx=2, ny=2):
    """
    Reversible spatial streaming oracle scaling as O(log N).
    """
    return build_d2q9_streaming_circuit(nx, ny)
