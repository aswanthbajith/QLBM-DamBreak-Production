"""
Approach A: Conventional D2Q9 + Global Carleman Linearization.
"""
import numpy as np
from carleman.operator import construct_discrete_carleman_step
from carleman.linearize import lift_state, project_state

class ApproachAGlobalCarleman:
    def __init__(self, nx=2, ny=2):
        self.nx = nx
        self.ny = ny
        self.n_nodes = nx * ny
        self.dim_linear = 9 * self.n_nodes
        self.dim_C = self.dim_linear + self.dim_linear**2
        
    def compile_step_matrix(self, S, M1, M2):
        """
        Compiles the full global Carleman step matrix of dimension 342 N.
        """
        F1 = S @ M1
        F2 = S @ M2
        return construct_discrete_carleman_step(F1, F2, self.dim_linear)
