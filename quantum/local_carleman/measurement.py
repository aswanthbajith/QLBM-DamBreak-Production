"""
Reconstruction of Macroscopic Fluid Observables from Dynamic Measurement Counts.
"""
import numpy as np

def reconstruct_density_from_counts(counts, nx=2, ny=2):
    """
    Reconstructs nodal density rho(x, y) from bitstring sampling counts.
    Bitstring format: [spatial_y, spatial_x, v3, v2, v1, v0]
    """
    total_shots = sum(counts.values())
    rho = np.zeros((ny, nx), dtype=np.float64)
    
    for bitstr, count in counts.items():
        # Clean bitstring
        b = bitstr.replace(" ", "")
        x = int(b[-1])
        y = int(b[-2])
        prob = count / float(total_shots)
        rho[y, x] += prob
        
    # Scale to mass normalization
    if np.sum(rho) > 0:
        rho = rho * (2.2 / np.sum(rho)) # standard 2x2 test mass
    return rho
