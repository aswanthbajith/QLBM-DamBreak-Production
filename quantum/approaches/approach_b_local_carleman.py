"""
Approach B: Local Carleman QLBM (PRE 113, 035307).
"""
from quantum.local_carleman.dynamic_circuit import build_dynamic_qlbm_step

class ApproachBLocalCarleman:
    def __init__(self, nx=2, ny=2):
        self.nx = nx
        self.ny = ny
        
    def build_circuit(self, timesteps=1):
        return build_dynamic_qlbm_step(self.nx, self.ny, timesteps=timesteps)
